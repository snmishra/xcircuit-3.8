/*----------------------------------------------------------------------*/
/* opengl.c --- routines defining graphics, whether OpenGL or X11	*/
/* Copyright (c) 2005  Tim Edwards, MultiGiG, Inc.			*/
/*----------------------------------------------------------------------*/

#ifdef OPENGL

/*----------------------------------------------------------------------*/
/*      written by Tim Edwards, 6/1/05    				*/
/*----------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <X11/Intrinsic.h>
#include <X11/StringDefs.h>

#include <GL/gl.h>
#include <GL/glx.h>
#include <GL/glu.h>

/*----------------------------------------------------------------------*/
/* Local includes							*/
/*----------------------------------------------------------------------*/

#ifdef TCL_WRAPPER
#include <tk.h>
#endif

#include "xcircuit.h"
#include "colordefs.h"

/*----------------------------------------------------------------------*/
/* Function prototype declarations                                      */
/*----------------------------------------------------------------------*/

#include "prototypes.h"

extern Colormap cmap;
extern int *appcolors;

extern char STIPDATA[STIPPLES][4];

extern float gl_line_limit, gl_point_limit;

/*----------------------------------------------------------------------*/
/* Global variables---							*/
/* Maintain current linewidth, because we need to pass this to the	*/
/* rendering routines, since we're duplicating all of the X calls,	*/
/* and they don't pass linewidth to the geometry drawing routines.	*/
/*----------------------------------------------------------------------*/

float cur_linewidth;

/*----------------------------------------------*/
/* Set color in OpenGL (this should be replaced	*/
/* for speed. . .)				*/
/*----------------------------------------------*/

void
SetForeground(Display *dpy, GC nullptr, int idx)
{
   XColor fgcolor;
   int red, green, blue;

   fgcolor.pixel = idx;
   fgcolor.flags = DoRed | DoGreen | DoBlue;

   XQueryColor(dpy, cmap, &fgcolor);

   glColor3us((GLushort)fgcolor.red, (GLushort)fgcolor.green,
		(GLushort)fgcolor.blue);
}

/*----------------------------------------------*/
/* Don't know if this is meaningful or not.	*/
/*----------------------------------------------*/

void
SetBackground(Display *dpy, GC nullptr, int idx)
{
   /* null proc */
}

/*------------------------------------------------------*/
/* Set drawing function					*/
/*------------------------------------------------------*/

void
SetFunction(Display *dpy, GC nullptr, int xfunction)
{
   switch (xfunction) {
      case GXcopy:
	 glDisable(GL_COLOR_LOGIC_OP);
	 /* Is it better to disable the logic op? */	
	 /*
	 glEnable(GL_COLOR_LOGIC_OP);
	 glLogicOp(GL_COPY);
	 */
	 break;
      case GXxor:
	 glEnable(GL_COLOR_LOGIC_OP);
	 glLogicOp(GL_XOR);
	 break;
   }
}

/*------------------------------------------------------*/
/* Set line attributes                                  */
/*------------------------------------------------------*/

void
SetLineAttributes(Display *dpy, GC nullptr, float lwidth,
	int ldash, int lcap, int lbevel)
{
   GLfloat glwidth = (lwidth <= 0) ? 1 : (GLfloat)lwidth;
   glLineWidth(glwidth);
   glPointSize(glwidth);

   cur_linewidth = (float)glwidth;

   if (lwidth > gl_line_limit)
      glDisable(GL_LINE_SMOOTH);
   else
      glEnable(GL_LINE_SMOOTH);

   switch (ldash) {
      case LineSolid:
	 glDisable(GL_LINE_STIPPLE);
	 break;
      case LineOnOffDash:
	 glEnable(GL_LINE_STIPPLE);
	 break;
   }
   /* Cap and Mitre not handled by OpenGL */
}

/*------------------------------------------------------*/
/* Set Line dash					*/
/*------------------------------------------------------*/

void
SetDashes(Display *dpy, GC nullptr, int offset, char dashlist[], int n)
{
   union {
      char dashbytes[2];
      u_short dashpat;
   } dashspec;

   dashspec.dashbytes[0] = dashlist[0];
   dashspec.dashbytes[1] = dashlist[1];

   glLineStipple((GLint)1, (GLushort)dashspec.dashpat);
}

/*------------------------------------------------------*/
/* Set Polygon fill stipple (optimize this!)		*/
/*------------------------------------------------------*/

void
SetStipple(Display *dpy, GC nullptr, int stipple)
{
   u_char stipdata[128];
   char *stipsrc = STIPDATA[stipple];
   char *stipdest = stipdata;
   int i;
   for (i = 0; i < 32; i++) {
      memcpy(stipdest, stipsrc, 4);
      stipdest += 4;
   }
   glPolygonStipple((GLubyte *)stipdata);
}

/*------------------------------------------------------*/
/* Set Polygon fill style				*/
/* (Currently there is no differentiating between the	*/
/* FillStippled and FillOpaqueStippled styles)		*/
/*------------------------------------------------------*/

void
SetFillStyle(Display *dpy, GC nullptr, int fillstyle)
{
   switch(fillstyle) {
      case FillSolid:
	 glDisable(GL_POLYGON_STIPPLE);
	 break;
      case FillStippled:
	 glEnable(GL_POLYGON_STIPPLE);
	 break;
      case FillOpaqueStippled:
	 glEnable(GL_POLYGON_STIPPLE);
	 break;
   }
}

/*------------------------------------------------------*/
/* Draw a line without endpoints			*/
/*------------------------------------------------------*/

void
DrawLineNoEndpoint(Display *dpy, Window win, GC nullptr,
	int x1, int y1, int x2, int y2)
{
   int i;
   GLdouble x, y;
   double theta, xmin, ymin, xmax, ymax, xoff, yoff;

   /* Simple line, if we are within the hardware's width */
   /* limit for lines.					 */

   if (cur_linewidth < gl_line_limit) {
      glBegin(GL_LINES);
      glVertex2i(x1, y1);
      glVertex2i(x2, y2);
      glEnd();
      return;
   }

   /* If we're outside the hardware's limit to draw	*/
   /* lines, then we revert to a (much slower)		*/
   /* quadrangle drawing routine.			*/

   glBegin(GL_QUADS);

   xmin = (double)x1;
   ymin = (double)y1;
   xmax = (double)x2;
   ymax = (double)y2;
   theta = atan2(ymax - ymin, xmax - xmin);
   xoff = cur_linewidth * cos(theta - 1.5708) / 2;
   yoff = cur_linewidth * sin(theta - 1.5708) / 2;

   x = (GLdouble)(xmax + xoff);
   y = (GLdouble)(ymax + yoff);
   glVertex2d(x, y);

   x = (GLdouble)(xmax - xoff);
   y = (GLdouble)(ymax - yoff);
   glVertex2d(x, y);

   x = (GLdouble)(xmin - xoff);
   y = (GLdouble)(ymin - yoff);
   glVertex2d(x, y);

   x = (GLdouble)(xmin + xoff);
   y = (GLdouble)(ymin + yoff);
   glVertex2d(x, y);

   glEnd();
}

/*------------------------------------------------------*/
/* Draw line (compatibility function for XDrawLine()	*/
/*------------------------------------------------------*/

void
DrawLine(Display *dpy, Window win, GC nullptr,
	int x1, int y1, int x2, int y2)
{
   /* Lines are capped with round ends. */
   /* (to-do: deal with the square end flag on lines) */
 
   DrawLineNoEndpoint(dpy, win, nullptr, x1, y1, x2, y2);
   DrawPoint(dpy, win, nullptr, x1, y1);
   DrawPoint(dpy, win, nullptr, x2, y2);
}

/*--------------------------------------------------------------*/
/* Draw multiple lines (compatibility function for XDrawLines()	*/
/* (Slight performance improvement over DrawLine by calling	*/
/* point-drawing routine only once in-between segments).	*/
/*--------------------------------------------------------------*/

void
DrawLines(Display *dpy, Window win, GC nullptr,
	XPoint *points, int npoints, int mode)
{
   int i;

   for (i = 0; i < npoints - 1; i++) {
      DrawLineNoEndpoint(dpy, win, nullptr, points[i].x, points[i].y,
		points[i + 1].x, points[i + 1].y);
      DrawPoint(dpy, win, nullptr, points[i].x, points[i].y);
   }
   DrawPoint(dpy, win, nullptr, points[i].x, points[i].y);
}

/*------------------------------------------------------*/
/* Draw point (compatibility function for XDrawPoint()	*/
/* To avoid the problem with OpenGL's inability to 	*/
/* render smooth circles at all zoom levels, we bypass	*/
/* the glPoint mechanism and use a tesselated polygon	*/
/* instead.						*/
/*------------------------------------------------------*/

void
DrawPoint(Display *dpy, Window win, GC nullptr, int x, int y)
{
   int i;
   double theta, delta, radius;
   GLdouble px, py;

   /* If we're below the OpenGL hardware limit on smooth point	*/
   /* drawing, then use the simple point-rendering routine.	*/

   if (cur_linewidth < gl_point_limit) {
      glBegin(GL_POINTS);
      glVertex2i(x, y);
      glEnd();
      return;
   }

   /* If we're above the OpenGL hardware limit on point size,	*/
   /* use a (much slower) 72-point polygon to render each dot.	*/
   /* This generally works well because at the scale where	*/
   /* the hardware can't render the point, it is unlikely that	*/
   /* there will be more than a handful of points visible in	*/
   /* the window.						*/

   radius = (double)(cur_linewidth / 2);
   theta = 0;
   delta = RADFAC * (360 / RSTEPS);

   glBegin(GL_POLYGON);
   for (i = 0; i < RSTEPS; i++) {
      px = (GLdouble)(x + radius * cos(theta));
      py = (GLdouble)(y + radius * sin(theta));
      theta += delta;
      glVertex2d(px, py);
   }
   glEnd();
}

/*----------------------------------------------------------------------*/
/* Helper function for GLU polygon tesselation intersections.		*/
/* This routine was arbitrarily scrapped together from information in	*/
/* the manpage for gluTessCallback().					*/
/*----------------------------------------------------------------------*/

void
myCombine(GLdouble coords[3], GLdouble *vertex_data[4],
	  GLfloat weight[4], GLdouble **outData)
{
    GLdouble *new = (GLdouble *)malloc(2 * sizeof(GLdouble));
    new[0] = coords[0];
    new[1] = coords[1];
    *outData = new;
}

/*----------------------------------------------------------------------*/
/* Draw a filled polygon (compatibility function for XFillPolygon()	*/
/*----------------------------------------------------------------------*/

void
FillPolygon(Display *dpy, Window win, GC nullptr, XPoint *points,
	int npoints, int shape, int mode)
{
   int i, j;
   static GLUtesselator *tess = NULL;
   static GLdouble *v;

   if (tess == NULL) {
      tess = gluNewTess();
      gluTessCallback(tess, GLU_TESS_BEGIN, (_GLUfuncptr)glBegin);
      gluTessCallback(tess, GLU_TESS_VERTEX, (_GLUfuncptr)glVertex2dv);
      gluTessCallback(tess, GLU_TESS_END, (_GLUfuncptr)glEnd);
      gluTessCallback(tess, GLU_TESS_COMBINE, (_GLUfuncptr)myCombine);
      v = (GLdouble *)malloc(2 * npoints * sizeof(GLdouble));
   }
   else {
      v = (GLdouble *)realloc(v, 2 * npoints * sizeof(GLdouble));
   }

   gluTessBeginPolygon(tess, NULL);
   gluTessBeginContour(tess);
   j = 0;
   for (i = 0; i < npoints; i++, j += 2) {
      v[j] = (GLdouble)points[i].x;
      v[j + 1] = (GLdouble)points[i].y;
      gluTessVertex(tess, &v[j], &v[j]);
   }
   gluTessEndContour(tess);
   gluTessEndPolygon(tess);
}

/*------------------------------------------------------*/
/* Render a background image				*/
/*------------------------------------------------------*/

void
backgroundbbox(int b)
{
   /* null proc for now . . . */
}

void
readbackground(FILE *f)
{
   /* null proc for now . . . */
}

void
savebackground(FILE *f, char *c)
{
   /* null proc for now . . . */
}

void
loadbackground()
{
   /* null proc for now . . . */
}

int
renderbackground()
{
   /* null proc for now . . . */
}

int
copybackground()
{
   /* null proc for now . . . */
}

int
reset_gs()
{
   /* This is a null proc because OpenGL doesn't use	*/
   /* ghostscript, and it's easier to make a null proc	*/
   /* than to #ifdef the calls.				*/

}

int
exit_gs()
{
   /* ditto */
}

/*-------------------------------------------------------------------------*/

#endif /* OPENGL */
