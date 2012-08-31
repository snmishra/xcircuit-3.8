/*----------------------------------------------------------------------*/
/* render.c --- Ghostscript rendering of background PostScript files	*/
/* Copyright (c) 2002  Tim Edwards, Johns Hopkins University        	*/
/* These routines work only if ghostscript is on the system.		*/
/*----------------------------------------------------------------------*/

/* We use OpenGL functions to read and scale images if OpenGL is enabled */
#ifndef OPENGL

/* #undef GS_DEBUG */
#define GS_DEBUG

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef XC_WIN32
#include <termios.h>
#include <unistd.h>
#endif
#include <time.h>
#ifndef XC_WIN32
#include <sys/wait.h>   /* for waitpid() */
#endif
#include <sys/types.h>
#include <signal.h>
#include <fcntl.h>

#ifndef XC_WIN32
#include <X11/Intrinsic.h>
#include <X11/StringDefs.h>
#include <X11/Xatom.h>
#else
#ifdef TCL_WRAPPER
#include <X11/Xatom.h>
#endif
#endif

/*------------------------------------------------------------------------*/
/* Local includes                                                         */
/*------------------------------------------------------------------------*/

#ifdef TCL_WRAPPER 
#include <tk.h>
#endif

#include "colordefs.h"
#include "xcircuit.h"

/*----------------------------------------------------------------------*/
/* Function prototype declarations                                      */
/*----------------------------------------------------------------------*/
#include "prototypes.h"

/*------------------------------------------------------------------------*/
/* External Variable definitions                                          */
/*------------------------------------------------------------------------*/

extern char _STR2[250], _STR[150];
extern Globaldata xobjs;
extern XCWindowData *areawin;
extern Display *dpy;
extern int *appcolors;
extern int number_colors;
extern colorindex *colorlist;
extern Cursor appcursors[NUM_CURSORS];

Pixmap bbuf = (Pixmap)NULL;	/* background buffer */
#ifdef DOUBLEBUFFER
extern Pixmap dbuf;
#endif

#ifndef HAVE_VFORK
#define vfork fork
#endif

int gs_state;		/* Track state of the renderer */

#define GS_INIT 0	/* Initial state; gs is idle. */
#define GS_PENDING 1	/* Drawing in progress; gs is busy. */
#define GS_READY 2	/* Drawing done; gs is waiting for "next". */

/*------------------------------------------------------*/
/* Global variable definitions				*/
/*------------------------------------------------------*/

Atom  gv, gvc, gvpage, gvnext, gvdone;
#ifndef _MSC_VER
pid_t gsproc = -1;	/* ghostscript process 			*/
#else
HANDLE gsproc = INVALID_HANDLE_VALUE;
#endif
int   fgs[2];		/* stdin pipe pair for ghostscript	*/
Window mwin = 0;	/* "false" window hack to get gs	*/
			/* process to capture ClientMessage	*/
			/* events.				*/

/*--------------------------------------------------------------*/
/* Preliminary in allowing generic PostScript backgrounds 	*/
/* via the ghostscript interpreter:  Set the GHOSTVIEW and	*/
/* GHOSTVIEW atoms, and set the GHOSTVIEW environtment		*/
/* variable.							*/
/*--------------------------------------------------------------*/

void ghostinit_local()
{
   sprintf(_STR, "%ld %d %d %d %d %d %g %g %d %d %d %d",
		0L, 0, 0, 0,
		areawin->width * 75 / 72,
		areawin->height * 75 / 72,
		75.0, 75.0, 0, 0, 0, 0);
   XChangeProperty(dpy, areawin->window, gv, XA_STRING, 8, PropModeReplace,
	_STR, strlen(_STR));
   sprintf(_STR, "%s %d %d", "Color", (int)FOREGROUND, (int)BACKGROUND);
   XChangeProperty(dpy, areawin->window, gvc, XA_STRING, 8, PropModeReplace,
	_STR, strlen(_STR));
   XSync(dpy, False);

   gs_state = GS_INIT;
}

/*------------------------------------------------------*/
/* Client message handler.  Called by either the Tk	*/
/* client message handler (see below) or the Xt handler	*/
/* (see xcircuit.c).					*/
/*							*/
/* Returns True if a client message was received from	*/
/* the ghostscript process, False if not.		*/
/*------------------------------------------------------*/

Boolean render_client(XEvent *eventPtr)
{
   if (eventPtr->xclient.message_type == gvpage) {
#ifdef GS_DEBUG
      fprintf(stdout, "Xcircuit: Received PAGE message from ghostscript\n");
#endif
      mwin = eventPtr->xclient.data.l[0];
      Wprintf("Background finished.");
      XDefineCursor(dpy, areawin->window, DEFAULTCURSOR);

      /* Mark this as the most recently rendered background, so we don't	*/
      /* have to render more than necessary.					*/
      areawin->lastbackground = xobjs.pagelist[areawin->page]->background.name;
      gs_state = GS_READY;
      drawarea(areawin->area, NULL, NULL);
   }
   else if (eventPtr->xclient.message_type == gvdone) {
#ifdef GS_DEBUG
      fprintf(stdout, "Xcircuit: Received DONE message from ghostscript\n");
#endif
      mwin = 0;
      gs_state = GS_INIT;
   } 
   else {
      char *atomname;

      atomname = XGetAtomName(dpy, eventPtr->xclient.message_type);
      if (atomname != NULL) {
	 fprintf(stderr, "Received client message using atom \"%s\"\n", atomname);
	 XFree(atomname);
      }
      return False;
   }
   return True;
}

/*------------------------------------------------------*/
/* Tk client handler procedure for the above routine.	*/
/*------------------------------------------------------*/

#ifdef TCL_WRAPPER

void handle_client(ClientData clientData, XEvent *eventPtr)
{
   if (render_client(eventPtr) == False)
      fprintf(stderr, "Xcircuit: Received unknown client message\n");
}

#endif

/*------------------------------------------------------*/
/* Global initialization				*/
/*------------------------------------------------------*/

void ghostinit()
{
   gv = XInternAtom(dpy, "GHOSTVIEW", False);
   gvc = XInternAtom(dpy, "GHOSTVIEW_COLORS", False);
   gvpage = XInternAtom(dpy, "PAGE", False);
   gvnext = XInternAtom(dpy, "NEXT", False);
   gvdone = XInternAtom(dpy, "DONE", False);

   ghostinit_local();

#ifdef TCL_WRAPPER
   Tk_CreateClientMessageHandler((Tk_ClientMessageProc *)handle_client);
#endif
}

/*------------------------------------------------------*/
/* Send a ClientMessage event				*/
/*------------------------------------------------------*/

void send_client(Atom msg)
{
   XEvent event;

   if (mwin == 0) return;	/* Have to wait for gs */
				/* to give us window # */

   event.xclient.type = ClientMessage;
   event.xclient.display = dpy;
   event.xclient.window = areawin->window;
   event.xclient.message_type = msg;
   event.xclient.format = 32;
   event.xclient.data.l[0] = mwin;
   event.xclient.data.l[1] = bbuf;
   XSendEvent(dpy, mwin, False, 0, &event);
   XFlush(dpy);
}

/*------------------------------------------------------*/
/* Ask ghostscript to produce the next page.		*/
/*------------------------------------------------------*/

void ask_for_next()
{
   if (gs_state != GS_READY) {
      /* If we're in the middle of rendering something, halt	*/
      /* immediately and start over.				*/
      if (gs_state == GS_PENDING)
	 reset_gs();
      return;
   }
   XSync(dpy, False);
   gs_state = GS_PENDING;
   send_client(gvnext);
#ifdef GS_DEBUG
   fprintf(stdout, "Xcircuit: Sent NEXT message to ghostscript\n");
#endif
}

/*--------------------------------------------------------*/
/* Start a ghostscript process and arrange the I/O pipes  */
/* (Commented lines cause ghostscript to relay its stderr */
/* to xcircuit's stderr)				  */
/*--------------------------------------------------------*/

void start_gs()
{
   int std_out[2], std_err[2], ret;
#ifdef XC_WIN32
   unsigned int pipe_size = 8196;
   int pipe_mode = _O_BINARY;
#endif
#ifdef HAVE_PUTENV
   static char env_str1[128], env_str2[64];
#endif

#ifdef TCL_WRAPPER
   if (bbuf != (Pixmap)NULL) Tk_FreePixmap(dpy, bbuf);
#ifdef DOUBLEBUFFER
   bbuf = Tk_GetPixmap(dpy, dbuf, areawin->width, areawin->height,
		Tk_Depth(areawin->area));
#else
   bbuf = Tk_GetPixmap(dpy, (Drawable)areawin->window,
		areawin->width, areawin->height,
		Tk_Depth(areawin->area));
#endif

#else	/* !TCL_WRAPPER */
   if (bbuf != (Pixmap)NULL) XFreePixmap(dpy, bbuf);
#ifdef DOUBLEBUFFER
   bbuf = XCreatePixmap(dpy, dbuf, areawin->width, areawin->height,
		DefaultDepthOfScreen(xcScreen(areawin->area))); 
#else
   bbuf = XCreatePixmap(dpy, areawin->window,
		areawin->width, areawin->height,
		DefaultDepthOfScreen(xcScreen(areawin->area))); 
#endif	/* DOUBLEBUFFER */
#endif  /* TCL_WRAPPER */

   XSync(dpy, False);

#ifndef XC_WIN32
   ret = pipe(fgs);
   ret = pipe(std_out);
#else
   ret = _pipe(fgs, pipe_size, pipe_mode);
   ret = _pipe(std_out, pipe_size, pipe_mode);
#endif
#ifndef GS_DEBUG
#ifndef XC_WIN32
   ret = pipe(std_err);
#else
   ret = _pipe(srd_err, pipe_size, pipe_mode);
#endif  /* XC_WIN32 */
#endif

   /* We need a complicated pipe here, with input going from xcircuit	*/
   /* to gs to provide scale/position information, and input going from */
   /* the background file to gs for rendering.				*/
   /* Here is not the place to do it.  Set up gs to take stdin as input.*/

#ifdef _MSC_VER
   if (gsproc == INVALID_HANDLE_VALUE) {
	 STARTUPINFO st_info;
	 PROCESS_INFORMATION pr_info;
	 char cmd[4096];

#ifdef HAVE_PUTENV
   	 sprintf(env_str1, "DISPLAY=%s", XDisplayString(dpy));
	 putenv(env_str1);
#ifdef DOUBLEBUFFER
   	 sprintf(env_str2, "GHOSTVIEW=%ld %ld", (long)areawin->window, (long)bbuf);
	 putenv(env_str2);
#else
	 sprintf(env_str2, "GHOSTVIEW=%ld", (long)areawin->window);
	 putenv(env_str2);
#endif
#else
	 setenv("DISPLAY", XDisplayString(dpy), True);
#ifdef DOUBLEBUFFER
	 sprintf(_STR, "%ld %ld", (long)areastruct.areawin, (long)bbuf);
	 setenv("GHOSTVIEW", _STR, True);
#else
 	 sprintf(_STR, "%ld", (long)areastruct.areawin);
	 setenv("GHOSTVIEW", _STR, True);
#endif
#endif

	 SetHandleInformation((HANDLE)_get_osfhandle(fgs[1]), HANDLE_FLAG_INHERIT, 0);
	 SetHandleInformation((HANDLE)_get_osfhandle(std_out[0]), HANDLE_FLAG_INHERIT, 0);
#ifndef GS_DEBUG
	 SetHandleInformation((HANDLE)_get_osfhandle(std_err[0]), HANDLE_FLAG_INHERIT, 0);
#endif

	 ZeroMemory(&st_info, sizeof(STARTUPINFO));
	 ZeroMemory(&pr_info, sizeof(PROCESS_INFORMATION));
	 st_info.cb = sizeof(STARTUPINFO);
	 st_info.dwFlags = STARTF_USESTDHANDLES;
	 st_info.hStdOutput = (HANDLE)_get_osfhandle(std_out[1]);
	 st_info.hStdInput = (HANDLE)_get_osfhandle(fgs[0]);
#ifndef GS_DEBUG
	 st_info.hStdError = (HANDLE)_get_osfhandle(std_err[1]);
#endif

	 snprintf(cmd, 4095, "%s -dNOPAUSE -", GS_EXEC);
	 if (CreateProcess(NULL, cmd, NULL, NULL, TRUE, 0, NULL, NULL, &st_info, &pr_info) == 0) {
		 Wprintf("Error: ghostscript not running");
		 return;
	 }
	 CloseHandle(pr_info.hThread);
	 gsproc = pr_info.hProcess;
   }
#else
   if (gsproc < 0) {  /* Ghostscript is not running yet */
      gsproc = vfork();
      if (gsproc == 0) {		/* child process (gs) */
#ifdef GS_DEBUG
         fprintf(stdout, "Calling %s\n", GS_EXEC);
#endif
	 close(std_out[0]);
#ifndef GS_DEBUG
  	 close(std_err[0]);
#endif
	 dup2(fgs[0], 0);
	 close(fgs[0]);
	 dup2(std_out[1], 1);
	 close(std_out[1]);
#ifndef GS_DEBUG
	 dup2(std_err[1], 2);
	 close(std_err[1]);
#endif

#ifdef HAVE_PUTENV
   	 sprintf(env_str1, "DISPLAY=%s", XDisplayString(dpy));
	 putenv(env_str1);
#ifdef DOUBLEBUFFER
   	 sprintf(env_str2, "GHOSTVIEW=%ld %ld", (long)areawin->window, (long)bbuf);
	 putenv(env_str2);
#else
	 sprintf(env_str2, "GHOSTVIEW=%ld", (long)areawin->window);
	 putenv(env_str2);
#endif
#else
	 setenv("DISPLAY", XDisplayString(dpy), True);
#ifdef DOUBLEBUFFER
	 sprintf(_STR, "%ld %ld", (long)areawin->window, (long)bbuf);
	 setenv("GHOSTVIEW", _STR, True);
#else
 	 sprintf(_STR, "%ld", (long)areawin->window);
	 setenv("GHOSTVIEW", _STR, True);
#endif
#endif
	 Flush(stderr);
         execlp(GS_EXEC, "gs", "-dNOPAUSE", "-", (char *)NULL);
	 gsproc = -1;
	 fprintf(stderr, "Exec of gs failed\n");
	 return;
      }
      else if (gsproc < 0) {
	 Wprintf("Error: ghostscript not running");
	 return;			/* error condition */
      }
   }
#endif
}

/*--------------------------------------------------------*/
/* Parse the background file for Bounding Box information */
/*--------------------------------------------------------*/

void parse_bg(FILE *fi, FILE *fbg) {
   char *bbptr;
   Boolean bflag = False;
   int llx, lly, urx, ury;
   char line_in[256];
   float psscale;

   psscale = getpsscale(xobjs.pagelist[areawin->page]->outscale, areawin->page);

   for(;;) {
      if (fgets(line_in, 255, fi) == NULL) {
         Wprintf("Error: end of file before end of insert.");
         return;
      }
      else if (strstr(line_in, "end_insert") != NULL) break;
	
      if (!bflag) {
	 if ((bbptr = strstr(line_in, "BoundingBox:")) != NULL) {
	    if (strstr(line_in, "(atend)") == NULL) {
	       bflag = True;
	       sscanf(bbptr + 12, "%d %d %d %d", &llx, &lly, &urx, &ury);
	       /* compute user coordinate bounds from PostScript bounds */
#ifdef GS_DEBUG
	       fprintf(stdout, "BBox %d %d %d %d PostScript coordinates\n",
			llx, lly, urx, ury);
#endif
	       llx = (int)((float)llx / psscale);
	       lly = (int)((float)lly / psscale);
	       urx = (int)((float)urx / psscale);
	       ury = (int)((float)ury / psscale);
#ifdef GS_DEBUG
	       fprintf(stdout, "BBox %d %d %d %d XCircuit coordinates\n",
			llx, lly, urx, ury);
#endif
	
	       xobjs.pagelist[areawin->page]->background.bbox.lowerleft.x = llx;
	       xobjs.pagelist[areawin->page]->background.bbox.lowerleft.y = lly;
	       xobjs.pagelist[areawin->page]->background.bbox.width = (urx - llx);
	       xobjs.pagelist[areawin->page]->background.bbox.height = (ury - lly);
	       if (fbg == (FILE *)NULL) break;
	    }
	 }
      }
      if (fbg != (FILE *)NULL) fputs(line_in, fbg);
   }
}

/*-------------------------------------------------------*/
/* Get bounding box information from the background file */
/*-------------------------------------------------------*/

void bg_get_bbox()
{
   FILE *fi;
   char *fname;

   fname = xobjs.pagelist[areawin->page]->background.name;
   if ((fi = fopen(fname, "r")) == NULL) {
      fprintf(stderr, "Failure to open background file to get bounding box info\n");
      return;
   }
   parse_bg(fi, (FILE *)NULL);
   fclose(fi);
}

/*------------------------------------------------------------*/
/* Adjust object's bounding box based on the background image */
/*------------------------------------------------------------*/

void backgroundbbox(int mpage)
{
   int llx, lly, urx, ury, tmp;
   objectptr thisobj = xobjs.pagelist[mpage]->pageinst->thisobject;
   psbkground *thisbg = &xobjs.pagelist[mpage]->background;

   llx = thisobj->bbox.lowerleft.x;
   lly = thisobj->bbox.lowerleft.y;
   urx = thisobj->bbox.width + llx;
   ury = thisobj->bbox.height + lly;

   if (thisbg->bbox.lowerleft.x < llx) llx = thisbg->bbox.lowerleft.x;
   if (thisbg->bbox.lowerleft.y < lly) lly = thisbg->bbox.lowerleft.y;
   tmp = thisbg->bbox.width + thisbg->bbox.lowerleft.x;
   if (tmp > urx) urx = tmp;
   tmp = thisbg->bbox.height + thisbg->bbox.lowerleft.y;
   if (tmp > ury) ury = tmp;

   thisobj->bbox.lowerleft.x = llx;
   thisobj->bbox.lowerleft.y = lly;
   thisobj->bbox.width = urx - llx;
   thisobj->bbox.height = ury - lly;
}

/*------------------------------------------------------*/
/* Read a background PostScript image from a file and	*/
/* store in a temporary file, passing that filename to	*/
/* the background property of the page.			*/
/*------------------------------------------------------*/

void readbackground(FILE *fi)
{
   FILE *fbg = (FILE *)NULL;
   int tfd;
   char *file_in = (char *)malloc(9 + strlen(xobjs.tempdir));

   /* "@" denotes a temporary file */
   sprintf(file_in, "@%s/XXXXXX", xobjs.tempdir);

#ifdef _MSC_VER
   tfd = mktemp(file_in + 1);
#else
   tfd = mkstemp(file_in + 1);
#endif
   if (tfd == -1) fprintf(stderr, "Error generating temporary filename\n");
   else {
      if ((fbg = fdopen(tfd, "w")) == NULL) {
	 fprintf(stderr, "Error opening temporary file \"%s\"\n", file_in + 1);
      }
   }

   /* Read the file to the restore directive or end_insertion */
   /* Skip restore directive and end_insertion command */

   parse_bg(fi, fbg);

   if (fbg != (FILE *)NULL) {
      fclose(fbg);
      register_bg(file_in);
   }
   free(file_in);
}

/*------------------------------------------------------*/
/* Save a background PostScript image to the output	*/
/* file by streaming directly from the background file	*/
/*------------------------------------------------------*/

void savebackground(FILE *fo, char *psfilename)
{
   FILE *psf;
   char *fname = psfilename;
   char line_in[256];

   if (fname[0] == '@') fname++;

   if ((psf = fopen(fname, "r")) == NULL) {
      fprintf(stderr, "Error opening background file \"%s\" for reading.\n", fname);
      return;
   }

   for(;;) {
      if (fgets(line_in, 255, psf) == NULL)
	 break;
      else
	 fputs(line_in, fo);
   }
   fclose(psf);
}

/*--------------------------------------------------------------*/
/* Set up a page to render a PostScript image when redrawing.	*/
/* This includes starting the ghostscript process if it has	*/
/* not already been started.  This routine does not draw the	*/
/* image, which is done on refresh.				*/
/*--------------------------------------------------------------*/

void register_bg(char *gsfile)
{
   if (gsproc < 0)
      start_gs();
   else
      reset_gs();

   xobjs.pagelist[areawin->page]->background.name =
		(char *) malloc(strlen(gsfile) + 1);
   strcpy(xobjs.pagelist[areawin->page]->background.name, gsfile);
}

/*------------------------------------------------------*/
/* Load a generic (non-xcircuit) postscript file as the */
/* background for the page.   This function is called	*/
/* by the file import routine, and so it completes by	*/
/* running zoomview(), which redraws the image and	*/
/* the page.						*/
/*------------------------------------------------------*/

void loadbackground()
{
   register_bg(_STR2);
   bg_get_bbox();
   updatepagebounds(topobject);
   zoomview(areawin->area, NULL, NULL);
}

/*------------------------------------------------------*/
/* Send text to the ghostscript renderer		*/
/*------------------------------------------------------*/

void send_to_gs(char *text)
{
#ifndef XC_WIN32
   write(fgs[1], text, strlen(text));
   tcflush(fgs[1], TCOFLUSH);
#else
   _write(fgs[1], text, (unsigned int)strlen(text));
#endif
#ifdef GS_DEBUG
   fprintf(stdout, "writing: %s", text);
#endif
}

/*------------------------------------------------------*/
/* Call ghostscript to render the background into the	*/
/* pixmap buffer.					*/
/*------------------------------------------------------*/

int renderbackground()
{
   char *bgfile;
   float psnorm, psxpos, psypos, defscale;
   float devres = 0.96; /* = 72.0 / 75.0, ps_units/in : screen_dpi */

   if (gsproc < 0) return -1;

   defscale = (xobjs.pagelist[areawin->page]->coordstyle == CM) ?
	CMSCALE : INCHSCALE;

   psnorm = areawin->vscale * (1.0 / defscale) * devres;

   psxpos = (float)(-areawin->pcorner.x) * areawin->vscale * devres;
   psypos = (float)(-areawin->pcorner.y) * areawin->vscale * devres
		+ ((float)areawin->height / 12.0);

   /* Conditions for re-rendering:  Must have a background specified */
   /* and must be on the page, not a library or other object.	     */

   if (xobjs.pagelist[areawin->page]->background.name == (char *)NULL)
      return -1;
   else if (areawin->lastbackground
		== xobjs.pagelist[areawin->page]->background.name) {
      return 0;
   }

   if (is_page(topobject) == -1)
      return -1;

   bgfile = xobjs.pagelist[areawin->page]->background.name;
   if (*bgfile == '@') bgfile++;

   /* Ask ghostscript to produce the next page */
   ask_for_next();

   /* Set the last background name to NULL; this will get the 	*/
   /* value when the rendering is done.				*/

   areawin->lastbackground = NULL;

   /* write scale and position to ghostscript 		*/
   /* and tell ghostscript to run the requested file	*/

   send_to_gs("/GSobj save def\n");
   send_to_gs("/setpagedevice {pop} def\n");
   send_to_gs("gsave\n");
   sprintf(_STR, "%3.2f %3.2f translate\n", psxpos, psypos);
   send_to_gs(_STR);
   sprintf(_STR, "%3.2f %3.2f scale\n", psnorm, psnorm);
   send_to_gs(_STR);
   sprintf(_STR, "(%s) run\n", bgfile);
   send_to_gs(_STR);
   send_to_gs("GSobj restore\n");
   send_to_gs("grestore\n");

#ifdef GS_DEBUG
   fprintf(stdout, "Rendering background from file \"%s\"\n", bgfile);
#endif
   Wprintf("Rendering background image.");
   XDefineCursor(dpy, areawin->window, WAITFOR);

   /* The page will be refreshed when we receive confirmation	*/
   /* from ghostscript that the buffer has been rendered.	*/

   return 0;
}

/*------------------------------------------------------*/
/* Copy the rendered background pixmap to the window.	*/
/*------------------------------------------------------*/

int copybackground()
{
   /* Don't copy if the buffer is not ready to use */
   if (gs_state != GS_READY)
      return -1;

   /* Only draw on a top-level page */
   if (is_page(topobject) == -1)
      return -1;

#ifdef DOUBLEBUFFER
   XCopyArea(dpy, bbuf, dbuf, areawin->gc, 0, 0,
             areawin->width, areawin->height, 0, 0);
#else
   XCopyArea(dpy, bbuf, areawin->window, areawin->gc, 0, 0,
             areawin->width, areawin->height, 0, 0);
#endif

   return 0;
}

/*------------------------------------------------------*/
/* Exit ghostscript. . . not so gently			*/
/*------------------------------------------------------*/

int exit_gs()
{
#ifdef _MSC_VER
   if (gsproc == INVALID_HANDLE_VALUE) return -1;	/* gs not running */
#else
   if (gsproc < 0) return -1;	/* gs not running */
#endif

#ifdef GS_DEBUG
   fprintf(stdout, "Waiting for gs to exit\n");
#endif
#ifndef _MSC_VER
   kill(gsproc, SIGKILL);
   waitpid(gsproc, NULL, 0);      
#else
   TerminateProcess(gsproc, -1);
#endif
#ifdef GS_DEBUG
   fprintf(stdout, "gs has exited\n");
#endif

   mwin = 0;
#ifdef _MSC_VER
   gsproc = INVALID_HANDLE_VALUE;
#else
   gsproc = -1;
#endif
   gs_state = GS_INIT;

   return 0;
}

/*------------------------------------------------------*/
/* Restart ghostscript					*/
/*------------------------------------------------------*/

int reset_gs()
{
#ifdef _MSC_VER
   if (gsproc == INVALID_HANDLE_VALUE) return -1;
#else
   if (gsproc < 0) return -1;
#endif

   exit_gs();
   ghostinit_local();
   start_gs();

   return 0;
}

#endif /* !OPENGL */

/*----------------------------------------------------------------------*/
