/*-----------------------------------------------------------------------*/
/* text.c --- text processing routines for xcircuit		 	 */
/* Copyright (c) 2002  Tim Edwards, Johns Hopkins University        	 */
/*-----------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>   /* for isprint() and isdigit() */

#ifndef _MSC_VER
#include <X11/Intrinsic.h>
#include <X11/StringDefs.h>
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

extern Display *dpy;
extern XCWindowData *areawin;
extern Globaldata xobjs;
extern short fontcount;
extern fontinfo *fonts;
extern int *appcolors;
extern colorindex *colorlist;
extern char _STR[150];

/* Global value of distance between characters in the font catalog */
short del;

#ifndef TCL_WRAPPER

/*----------------------------------------------------------------------*/
/* Evaluation of expression types in strings (non-Tcl version---these	*/
/* are PostScript expressions).						*/
/*									*/
/* For now, expressions are just copied as-is, without evaluation.	*/
/* An allocated string is returned, and it is the responsibility of the	*/
/* calling routine to free it.						*/
/*----------------------------------------------------------------------*/

char *evaluate_expr(objectptr thisobj, oparamptr ops, objinstptr pinst)
{
   if (ops->type != XC_EXPR) return NULL;
   return strdup(ops->parameter.expr);
}

#endif

/*----------------------------------------------------------------------*/
/* Determine if a label contains a parameter.				*/
/*----------------------------------------------------------------------*/

Boolean hasparameter(labelptr curlabel)
{
   stringpart *chrptr;

   for (chrptr = curlabel->string; chrptr != NULL; chrptr = chrptr->nextpart)
      if (chrptr->type == PARAM_START)
         return True;

   return False;
}

/*----------------------------------------------------------------------*/
/* Join selected labels together.					*/
/*----------------------------------------------------------------------*/

void joinlabels()
{
  /* genericptr *genobj; (jdk) */
   short *jl;
   stringpart *endpart;
   /* int tpos; (jdk) */
   labelptr dest, source;

   if (areawin->selects < 2) {
      Wprintf("Not enough labels selected for joining");
      return;
   }

   XcSetFunction(GXcopy);
   XSetForeground(dpy, areawin->gc, BACKGROUND);

   for (jl = areawin->selectlist; jl < areawin->selectlist +
		areawin->selects; jl++) {
      if (SELECTTYPE(jl) == LABEL) {
	 dest = SELTOLABEL(jl);
	 UDrawString(dest, DOFORALL, areawin->topinstance);
	 for (endpart = dest->string; endpart->nextpart != NULL; endpart =
			endpart->nextpart);
	 break;
      }
   }
      
   for (++jl; jl < areawin->selectlist + areawin->selects; jl++) {
      if (SELECTTYPE(jl) == LABEL) {
	 source = SELTOLABEL(jl);
	 UDrawString(source, DOFORALL, areawin->topinstance);
	 endpart->nextpart = source->string;
	 for (; endpart->nextpart != NULL; endpart = endpart->nextpart);
	 free(source);
	 removep(jl, 0);
         reviseselect(areawin->selectlist, areawin->selects, jl);
      }
   }

   XSetForeground(dpy, areawin->gc, dest->color);
   UDrawString(dest, dest->color, areawin->topinstance);

   incr_changes(topobject);
   clearselects();
}

/*----------------------------------------------------------------------*/
/* Insert a new segment into a string					*/
/*----------------------------------------------------------------------*/

stringpart *makesegment(stringpart **strhead, stringpart *before)
{
   stringpart *newptr, *lastptr, *nextptr;

   newptr = (stringpart *)malloc(sizeof(stringpart));
   newptr->data.string = NULL;

   if (before == *strhead) {	/* insert at beginning */
      newptr->nextpart = *strhead;
      *strhead = newptr;
   }
   else {				/* otherwise */
      for(lastptr = *strhead; lastptr != NULL;) {
	 nextptr = nextstringpart(lastptr, areawin->topinstance);
	 if (nextptr == before) {
	    if (lastptr->type == PARAM_START) {
	       oparamptr obs = NULL;
	       char *key = lastptr->data.string;
	       obs = find_param(areawin->topinstance, key);
	       if (obs == NULL) {
		  Wprintf("Error:  Bad parameter \"%s\"!", key);
	       } else {
	          obs->parameter.string = newptr;	/* ?? */
	       }
	    }
	    else {
	       lastptr->nextpart = newptr;
	    }
	    newptr->nextpart = nextptr;
	    break;
         }
	 else if (lastptr->nextpart == before && lastptr->type == PARAM_START) {
	    lastptr->nextpart = newptr;
	    newptr->nextpart = before;
	    break;
	 }
	 lastptr = nextptr;
      }
   }
   return newptr;
}

/*----------------------------------------------------------------------*/
/* Split a string across text segments					*/
/*----------------------------------------------------------------------*/

stringpart *splitstring(int tpos, stringpart **strtop, objinstptr localinst)
{
   int locpos, slen;
   stringpart *newpart, *ipart;

   ipart = findstringpart(tpos, &locpos, *strtop, localinst);
   if (locpos > 0) {        /* split the string */
      newpart = makesegment(strtop, ipart);
      newpart->type = TEXT_STRING;
      newpart->data.string = ipart->data.string;
      slen = strlen(newpart->data.string) - locpos;
      ipart->data.string = (u_char *)malloc(slen + 1);
      strncpy(ipart->data.string, newpart->data.string + locpos, slen  + 1);
      *(newpart->data.string + locpos) = '\0';
   }
   else newpart = ipart;

   return newpart;
}

/*----------------------------------------------------------------------*/
/* Get the next string part, linking to a parameter if necessary	*/
/*----------------------------------------------------------------------*/

stringpart *nextstringpartrecompute(stringpart *strptr, objinstptr thisinst)
{
   stringpart *nextptr = strptr->nextpart;

   if (strptr->type == PARAM_START)
      nextptr = linkstring(thisinst, strptr, TRUE);
   else if (strptr->type == PARAM_END) {
      strptr->nextpart = NULL;

      /* Parameters that have a non-NULL entry in data have	*/
      /* been promoted from an expression or numerical value	*/
      /* to a string.  The memory allocated for this string	*/
      /* should be free'd.					*/

      if (strptr->data.string != (u_char *)NULL) {
	 fprintf(stderr, "Non-NULL data in PARAM_END segment\n");
	 free(strptr->data.string);
	 strptr->data.string = (u_char *)NULL;
      }
   }
   return nextptr;
}

/*----------------------------------------------------------------------*/
/* Same as the above routine, but don't recompute expression parameters	*/
/* when encountered.  Use the previously generated result.		*/
/*----------------------------------------------------------------------*/

stringpart *nextstringpart(stringpart *strptr, objinstptr thisinst)
{
   stringpart *nextptr = strptr->nextpart;

   if (strptr->type == PARAM_START)
      nextptr = linkstring(thisinst, strptr, FALSE);
   else if (strptr->type == PARAM_END) {
      strptr->nextpart = NULL;
      if (strptr->data.string != (u_char *)NULL) {
	 fprintf(stderr, "Non-NULL data in PARAM_END segment\n");
	 free(strptr->data.string);
	 strptr->data.string = (u_char *)NULL;
      }
   }
   return nextptr;
}

/*----------------------------------------------------------------------*/
/* Remove a string part from the string					*/
/*----------------------------------------------------------------------*/

stringpart *deletestring(stringpart *dstr, stringpart **strtop, objinstptr thisinst)
{
   stringpart *strptr = NULL, *nextptr;
   char *key;
   oparamptr ops;

   if (dstr == *strtop)
      *strtop = dstr->nextpart;
   else {
      strptr = *strtop;
      while (strptr != NULL) {
	 nextptr = nextstringpart(strptr, thisinst);
	 if (nextptr == dstr) break;
	 strptr = nextptr;
      }
      if (strptr == NULL)
	 return NULL;

      /* If this is the begining of a parameter, then we have to figure */
      /* out if it's an instance or a default, and change the pointer	*/
      /* to the parameter in the parameter list, accordingly.		*/

      else if ((strptr->type == PARAM_START) && (thisinst != NULL)) {
	 key = strptr->data.string;
	 ops = find_param(thisinst, key);
	 if (ops == NULL) {
	    Fprintf(stderr, "Error in deletestring:  Bad parameter %s found\n", key); 
	 }
	 else {
	    switch(ops->type) {
	       case XC_STRING:
		  ops->parameter.string = dstr->nextpart;
		  break;
	       default:
		  /* What to be done here? */
		  break;
	    }
	 }
      }
      /* If this is the end of a parameter, we have to link the		*/
      /* PARAM_START, not the PARAM_END, which has already been nulled.	*/ 
      else if (strptr->type == PARAM_END) {
	 for (strptr = *strtop; strptr != NULL; strptr = strptr->nextpart) {
	    if (strptr->nextpart == dstr) {
	       strptr->nextpart = dstr->nextpart;
	       break;
	    }
         }
      }
      else
	 strptr->nextpart = dstr->nextpart;
   }
   if (dstr->type == TEXT_STRING)
      free(dstr->data.string);
   free(dstr);

   /* attempt to merge, if legal */
   if (strptr)
      mergestring(strptr);

   return strptr;
}

/*----------------------------------------------------------------------*/
/* Merge string parts at boundary, if parts can be legally merged	*/
/* If the indicated string part is text and the part following the	*/
/* indicated string part is also text, merge the two.  The indicated	*/
/* string part is returned, and the following part is freed.		*/
/*									*/
/* (Fixes thanks to Petter Larsson 11/17/03)				*/
/*----------------------------------------------------------------------*/

stringpart *mergestring(stringpart *firststr)
{
   stringpart *nextstr = NULL;

   if (firststr) nextstr = firststr->nextpart;
   if (nextstr != NULL) {
      if (firststr->type == TEXT_STRING && nextstr->type == TEXT_STRING) {
         firststr->nextpart = nextstr->nextpart;
         firststr->data.string = (char *)realloc(firststr->data.string,
		1 + strlen(firststr->data.string) + strlen(nextstr->data.string));
         strcat(firststr->data.string, nextstr->data.string);
         free(nextstr->data.string);
         free(nextstr);
      }
   }
   return firststr;
}

/*----------------------------------------------------------------------*/
/* Link a parameter to a string						*/
/* If compute_exprs is TRUE, then we should recompute any expression	*/
/* parameters encountered.  If FALSE, then we assume that all		*/
/* expressions have been computed previously, and may use the recorded	*/
/* instance value.							*/
/*									*/
/* 11/20/06---changed to allow two different static strings to save	*/
/* promoted results.  This is necessary because we may be comparing	*/
/* two promoted results in, e.g., stringcomprelaxed(), and we don't	*/
/* want to overwrite the first result with the second.			*/
/*----------------------------------------------------------------------*/

stringpart *linkstring(objinstptr localinst, stringpart *strstart,
	Boolean compute_exprs)
{
   char *key;
   stringpart *tmpptr, *nextptr = NULL;
   static stringpart *promote[2] = {NULL, NULL};
   static unsigned char pidx = 0;
   oparamptr ops;

   if (strstart->type != PARAM_START) return NULL;

   key = strstart->data.string;

   /* In case of no calling instance, always get the default from the	*/
   /* current page object.						*/

   if (localinst == NULL) {
      ops = match_param(topobject, key);
      if (ops == NULL)
	 return NULL;
   }
   else {
      ops = find_param(localinst, key);
      if (ops == NULL) {
	 /* We get here in cases where the object definition is being read,	*/
	 /* and there is no instance of the object to link to.  In that	*/
	 /* case, we ignore parameters and move on to the next part.		*/
	 return strstart->nextpart;
      }
   }

   if (ops->type != XC_STRING) {

      if (promote[pidx] == NULL) {
         /* Generate static string for promoting numerical parameters */
         tmpptr = makesegment(&promote[pidx], NULL);
         tmpptr->type = TEXT_STRING;
         tmpptr = makesegment(&promote[pidx], NULL);
         tmpptr->type = PARAM_END;
      }
      else {
	 if (promote[pidx]->data.string != NULL) {
	    free(promote[pidx]->data.string);
	    promote[pidx]->data.string = NULL;
	 }
      }

      /* Promote numerical type to string */
      if (ops->type == XC_INT) {
	 promote[pidx]->data.string = (char *)malloc(13);
	 sprintf(promote[pidx]->data.string, "%12d", ops->parameter.ivalue);
         nextptr = promote[pidx++];
      }
      else if (ops->type == XC_FLOAT) {
	 promote[pidx]->data.string = (char *)malloc(13);
	 sprintf(promote[pidx]->data.string, "%g", (double)(ops->parameter.fvalue));
         nextptr = promote[pidx++];
      }
      else {	/* ops->type == XC_EXPR */
	 oparamptr ips;
	 if (!compute_exprs && (ips = match_instance_param(localinst, key))
		!= NULL && (ips->type == XC_STRING)) {
	    nextptr = ips->parameter.string;
	    promote[pidx]->data.string = NULL;
	 }
	 else {
	    promote[pidx]->data.string = evaluate_expr(((localinst == NULL) ?
			topobject : localinst->thisobject), ops, localinst);
	    if (promote[pidx]->data.string != NULL)
               nextptr = promote[pidx++];
	    else
	       nextptr = NULL;
	 }
      }
      pidx &= 0x1;	/* pidx toggles between 0 and 1 */
   }
   else
      nextptr = ops->parameter.string;

   /* If the parameter exists, link the end of the parameter back to	*/
   /* the calling string.						*/

   if (nextptr != NULL) {
      tmpptr = nextptr;
      while (tmpptr->type != PARAM_END)
	 if ((tmpptr = tmpptr->nextpart) == NULL)
	    return NULL;
      tmpptr->nextpart = strstart->nextpart;
      return nextptr;
   }
   return NULL;
}

/*----------------------------------------------------------------------*/
/* Find the last font used prior to the indicated text position		*/
/*----------------------------------------------------------------------*/

int findcurfont(int tpos, stringpart *strtop, objinstptr thisinst)
{
   stringpart *curpos;
   int cfont = -1;
   stringpart *strptr;

   curpos = findstringpart(tpos, NULL, strtop, thisinst);
   for (strptr = strtop; (strptr != NULL) && (strptr != curpos);
		strptr = nextstringpart(strptr, thisinst))
      if (strptr->type == FONT_NAME)
         cfont = strptr->data.font;

   return cfont;
}

/*----------------------------------------------------------------------*/
/* Return a local position and stringpart for the first occurrence of	*/
/* "substring" in the the indicated xcircuit string.  If non-NULL,	*/
/* "locpos" is set to the position of the substring in the stringpart,	*/
/* or -1 if the text was not found.  Text cannot cross stringpart	*/
/* boundaries (although this should be allowed).			*/
/*----------------------------------------------------------------------*/

stringpart *findtextinstring(char *search, int *locpos, stringpart *strtop,
	objinstptr localinst)
{
   stringpart *strptr = strtop;
   char *strstart;

   for (strptr = strtop; strptr != NULL; strptr = nextstringpart(strptr, localinst)) {
      if ((strptr->type == TEXT_STRING) && strptr->data.string) {
	 strstart = strstr(strptr->data.string, search);
	 if (strstart != NULL) {
	    if (locpos != NULL)
	       *locpos = (int)(strstart - (char *)strptr->data.string);
	    return strptr;
	 }
      }
   }
   if (locpos != NULL) *locpos = -1;
   return NULL;
}

/*----------------------------------------------------------------------*/
/* Return a local position and stringpart for "tpos" positions into	*/
/* the indicated string.  Position and stringpart are for the character */
/* or command immediately preceding "tpos"				*/
/*----------------------------------------------------------------------*/

stringpart *findstringpart(int tpos, int *locpos, stringpart *strtop,
	objinstptr localinst)
{
   stringpart *strptr = strtop;
   int testpos = 0, tmplen;

   for (strptr = strtop; strptr != NULL; strptr = nextstringpart(strptr, localinst)) {
      if ((strptr->type == TEXT_STRING) && strptr->data.string) {
	 tmplen = strlen(strptr->data.string);
	 if (testpos + tmplen > tpos) {
	    if (locpos != NULL) *locpos = (tpos - testpos);
	    return strptr;
	 }
	 else testpos += tmplen - 1;
      }
      if (locpos != NULL) *locpos = -1;
      if (testpos >= tpos) return strptr;

      testpos++;
   }
   return NULL;
}

/*----------------------------------------------------------------------*/
/* The following must be in an order matching the "Text string part	*/
/* types" defined in xcircuit.h. 					*/
/*----------------------------------------------------------------------*/

static char *nonprint[] = {
	"Text", "Subscript", "Superscript", "Normalscript",
	"Underline", "Overline", "Noline",
	"Tab_Stop", "Tab_Forward", "Tab_Backward",
	"Margin_Stop", "Halfspace", "Quarterspace", "<Return>",
	"Font", "Scale", "Color", "Kern", 
        "Parameter", ">", "Net_Name", "Error", NULL}; /* (jdk) */

/*----------------------------------------------------------------------*/
/* charprint():  							*/
/* Write a printable version of the character or command at the 	*/
/* indicated string part and position.					*/
/*----------------------------------------------------------------------*/

void charprint(char *sout, stringpart *strptr, int locpos)
{
   char sc;
 
   switch (strptr->type) {
      case TEXT_STRING:
	 if (strptr->data.string) {
            if (locpos > strlen(strptr->data.string)) {
	       strcpy(sout, "<ERROR>");
	    }
            else sc = *(strptr->data.string + locpos);
            if (isprint(sc))
	       sprintf(sout, "%c", sc);
            else
	       sprintf(sout, "/%03o", (u_char)sc);
	 }
	 else
	    *sout = '\0';
	 break;
      case FONT_NAME:
	 sprintf(sout, "Font=%s", (strptr->data.font >= fontcount) ?
		"(unknown)" : fonts[strptr->data.font].psname);
	 break;
      case FONT_SCALE:
	 sprintf(sout, "Scale=%3.2f", strptr->data.scale);
	 break;
      case KERN:
	 sprintf(sout, "Kern=(%d,%d)", strptr->data.kern[0], strptr->data.kern[1]);
	 break;
      case PARAM_START:
	 sprintf(sout, "Parameter(%s)<", strptr->data.string);
	 break;
      default:
         strcpy(sout, nonprint[strptr->type]);
	 break;
   }
}

/*----------------------------------------------------------------------*/
/* Print a string (allocates memory for the string; must be freed by	*/
/* the calling routine).						*/
/*----------------------------------------------------------------------*/

char *xcstringtostring(stringpart *strtop, objinstptr localinst, Boolean textonly)
{
   stringpart *strptr;
   int pos = 0, locpos;
   char *sout;

   sout = (char *)malloc(1);
   sout[0] = '\0';

   while ((strptr = findstringpart(pos++, &locpos, strtop, localinst)) != NULL) {
      if (!textonly || strptr->type == TEXT_STRING) {
         charprint(_STR, strptr, locpos);
         sout = (char *)realloc(sout, strlen(sout) + strlen(_STR) + 1);
         strcat(sout, _STR);
      }
      /* Overbar on schematic names is translated to logical-NOT ("!") */
      else if (textonly && strptr->type == OVERLINE) {
         sout = (char *)realloc(sout, strlen(sout) + 2);
         strcat(sout, "!");
      }
   }
   return sout;
}

/*----------------------------------------------------------------------*/
/* Wrappers for xcstringtostring():					*/
/*  stringprint() includes information on text controls appropriate	*/
/*  for printing in the message window (charreport())			*/
/*----------------------------------------------------------------------*/

char *stringprint(stringpart *strtop, objinstptr localinst)
{
   return xcstringtostring(strtop, localinst, False);
}

/*----------------------------------------------------------------------*/
/*  textprint() excludes text controls, resulting in a string 		*/
/*  appropriate for netlist information, or for promoting a string	*/
/*  parameter to a numeric type.					*/
/*----------------------------------------------------------------------*/

char *textprint(stringpart *strtop, objinstptr localinst)
{
   return xcstringtostring(strtop, localinst, True);
}

/*----------------------------------------------------------------------*/
/* textprintsubnet() is like textprint(), except that strings in bus	*/
/* notation are reduced to just the single subnet.			*/
/*----------------------------------------------------------------------*/

char *textprintsubnet(stringpart *strtop, objinstptr localinst, int subnet)
{
   char *newstr, *busptr, *endptr, *substr;

   newstr = xcstringtostring(strtop, localinst, True);
   if (subnet >= 0) {
      busptr = strchr(newstr, areawin->buschar);
      if (busptr != NULL) {
	 endptr = find_delimiter(busptr);
	 if (endptr != NULL) {
	    if (busptr == newstr)
	       sprintf(newstr, "%d", subnet);
	    else {
	       substr = strdup(newstr);
	       busptr++;
	       sprintf(substr + (int)(busptr - newstr), "%d%s", subnet, endptr);
	       free(newstr);
	       return substr;
	    }
	 }
      }
      else {
	 /* Promote a non-bus label to a bus label */
	 substr = malloc(10 + strlen(newstr));
	 strcpy(substr, newstr);
	 endptr = substr;
	 while ((*endptr) != '\0') endptr++;
	 sprintf(endptr, "%c%d%c", areawin->buschar, subnet,
		standard_delimiter_end(areawin->buschar));
	 free(newstr);
	 return substr;
      }
   }
   return newstr;
}

/*----------------------------------------------------------------------*/
/* Another variant:  Print a subnet list according to the entries in	*/
/* a netlist (Genericlist *) pointer.  This includes the condition in	*/
/* which the list is a single wire, not a bus.  If "pinstring" is non-	*/
/* NULL, it will be used as the name of the subnet.  Otherwise, 	*/
/* "prefix" will be used, and will be appended with the net ID of the	*/
/* first net in the sublist to make the identifier unique.		*/
/*----------------------------------------------------------------------*/

char *textprintnet(char *prefix, char *pinstring, Genericlist *sublist)
{
   char *newstr, *sptr;
   buslist *sbus;
   int i;

   if (sublist->subnets == 0) {
      newstr = (char *)malloc(strlen(prefix) + 10); 
      sprintf(newstr, "%s%d", prefix, sublist->net.id);
   }
   else {	/* just make a comma-separated list */
      newstr = (char *)malloc(strlen(prefix) + 20 + 3 * sublist->subnets);
      sbus = sublist->net.list;
      sprintf(newstr, "%s%d%c", prefix, sbus->netid, areawin->buschar);
      for (i = 0; i < sublist->subnets; i++) {
	 sbus = sublist->net.list + i;
	 sptr = newstr + strlen(newstr);
	 if (i != 0)
	    strcat(sptr++, ",");
	 sprintf(sptr, "%d", sbus->subnetid);
      }
      sptr = newstr + strlen(newstr);
      sprintf(sptr, "%c", standard_delimiter_end(areawin->buschar));
   }
   return newstr;
}

/*----------------------------------------------------------------------*/
/* Test equivalence of the text string parts of a label with the	*/
/* indicated char * string.						*/
/*									*/
/* Return 0 if the strings match.  Return 1 or the result of strcmp()	*/
/* on the first non-matching substring text segment if the strings	*/
/* don't match.								*/
/*									*/
/* If "exact" is True, requires an exact match, otherwise requires	*/
/* that the label only match text to the length of text.		*/
/*----------------------------------------------------------------------*/

int textcompx(stringpart *string, char *text, Boolean exact, objinstptr localinst)
{
   stringpart *strptr;
   char *tptr = text;
   char *sptr;
   int rval, llen = strlen(text), slen;
   Boolean has_text = FALSE;

   for (strptr = string; strptr != NULL; strptr = nextstringpart(strptr, localinst)) {
      if (strptr->type == TEXT_STRING) {
	 has_text = TRUE;
	 sptr = strptr->data.string;
	 slen = min(strlen(sptr), llen);
	 llen -= slen;
	 if (!exact && (rval = strncmp(sptr, tptr, slen)))
	    return rval;
	 else if (exact && (rval = strcmp(sptr, tptr)))
	    return rval;
	 else if (!exact && (llen == 0))
	    return 0;
	 else
	    tptr += slen;
      }
   }

   /* Check condition that no text was encountered in the xcircuit string */
   return ((llen > 0) && !has_text) ? 1 : 0;
}

/*----------------------------------------------------------------------*/
/* Wrappers for textcompx(), equivalent to strcmp() and strncmp().	*/
/*----------------------------------------------------------------------*/

int textcomp(stringpart *string, char *text, objinstptr localinst)
{
   return textcompx(string, text, True, localinst);
}

/*----------------------------------------------------------------------*/

int textncomp(stringpart *string, char *text, objinstptr localinst)
{
   return textcompx(string, text, False, localinst);
}

/*----------------------------------------------------------------------*/
/* Test equivalence of two label strings				*/
/*----------------------------------------------------------------------*/

int stringcomp(stringpart *string1, stringpart *string2)
{
   stringpart *strptr1, *strptr2;

   for (strptr1 = string1, strptr2 = string2; strptr1 != NULL && strptr2 != NULL;
		strptr1 = strptr1->nextpart, strptr2 = strptr2->nextpart) {
      if (strptr1->type != strptr2->type)
	 return 1;
      else {
         switch (strptr1->type) {
	    case TEXT_STRING:
	       if (strptr1->data.string && strptr2->data.string) {
	          if (strcmp(strptr1->data.string, strptr2->data.string))
		     return 1;
	       }
	       else if (strptr1->data.string || strptr2->data.string)
		  return 1;
	       break;
	    case FONT_SCALE:
	       if (strptr1->data.scale != strptr2->data.scale) return 1;
	       break;
	    case FONT_COLOR:
	       if (strptr1->data.color != strptr2->data.color) return 1;
	       break;
	    case FONT_NAME:
	       if (strptr1->data.font != strptr2->data.font) return 1;
	       break;
	    case KERN:
	       if (strptr1->data.kern[0] != strptr2->data.kern[0] ||
		   strptr1->data.kern[1] != strptr2->data.kern[1]) return 1;
	       break;
	 }
      }
   }

   /* One string continues after the other ends. . . */ 
   if (strptr1 != NULL || strptr2 != NULL) return 1;
   return 0;
}

/*----------------------------------------------------------------------*/
/* Test if the specified font is in the "Symbol" font family.		*/
/*----------------------------------------------------------------------*/

Boolean issymbolfont(int fontnumber)
{
   if (!strcmp(fonts[fontnumber].family, "Symbol")) return True;
   return False;
}

/*----------------------------------------------------------------------*/
/* Test if the specified font is in the "Helvetica" font family.	*/
/* SVG uses this to make sure it scales down the font by 7/8 to match	*/
/* our internal vectors, and to use "oblique" for the style instead of	*/
/* "italic".								*/
/*----------------------------------------------------------------------*/

Boolean issansfont(int fontnumber)
{
   if (!strcmp(fonts[fontnumber].family, "Helvetica")) return True;
   return False;
}

/*----------------------------------------------------------------------*/
/* Test if the specified font is ISO-Latin1 encoding			*/
/*----------------------------------------------------------------------*/

Boolean isisolatin1(int fontnumber)
{
   if ((fonts[fontnumber].flags & 0xf80) == 0x100) return True;
   return False;
}

/*----------------------------------------------------------------------*/
/* For a label representing a single bus subnet, return the index of	*/
/* the subnet.								*/
/*----------------------------------------------------------------------*/

int sub_bus_idx(labelptr thislab, objinstptr thisinst)
{
   stringpart *strptr;
   char *busptr;
   int busidx;

   for (strptr = thislab->string; strptr != NULL; strptr =
		nextstringpart(strptr, thisinst)) {
      if (strptr->type == TEXT_STRING) {
	 if ((busptr = strchr(strptr->data.string, areawin->buschar)) != NULL) {
	    if (sscanf(++busptr, "%d", &busidx) == 1)
	       return busidx;
	 }
	 if (sscanf(strptr->data.string, "%d", &busidx) == 1)
	    return busidx;
      }
   }
   return -1;
}

/*----------------------------------------------------------------------*/
/* The following routine is like sub_bus_idx but returns TRUE or FALSE	*/
/* depending on whether the label was determined to be in bus notation	*/
/* or not.  Note that sub_bux_idx may be run on sub-bus names (those	*/
/* that are internally generated from labels in bus notation), but	*/
/* pin_is_bus should not, because pin numbers in bus notation get the	*/
/* bus delimiters stripped from them.					*/
/*----------------------------------------------------------------------*/

Boolean pin_is_bus(labelptr thislab, objinstptr thisinst)
{
   stringpart *strptr;
   char *busptr;
   /* int busidx; (jdk) */
   Boolean found_delimiter = FALSE;

   for (strptr = thislab->string; strptr != NULL; strptr =
		nextstringpart(strptr, thisinst)) {
      if (strptr->type == TEXT_STRING) {
	 if ((busptr = strchr(strptr->data.string, areawin->buschar)) != NULL) {
	    if (isdigit(*(++busptr)))
	       return TRUE;
	    else
	       found_delimiter = TRUE;
	 }
	 else if (found_delimiter == TRUE) {
	    return (isdigit(*(strptr->data.string))) ? TRUE : FALSE;
	 }
      }
   }
   return FALSE;
}

/*----------------------------------------------------------------------*/
/* When encountering a label with bus notation, create a list of	*/
/* subnets belonging to the bus.  Return the list as a pointer to a	*/
/* Genericlist structure.  This structure is statically allocated and	*/
/* is expected to have its contents copied into the target netlist	*/
/* element.								*/
/*									*/
/* Unlike the above routine, this routine prints the original string	*/
/* into a char* array using textprint() so that escape sequences are	*/
/* removed and will not affect the result.				*/
/*									*/
/* To speed things up, the calling routine should have already called	*/
/* pin_is_bus() to determine if the label does indeed represent a bus.	*/
/* break_up_bus() is much slower in determining this.  If break_up_bus	*/
/* is passed a string that cannot be identified as a bus, then it	*/
/* returns a NULL pointer.						*/
/*									*/
/* If netlist points to a structure with no subnets, then its net ID	*/
/* is the starting point for the nets returned by break_up_bus.  	*/
/* Otherwise, netlist is assumed to be a valid netlist for a bus that	*/
/* matches "blab", and we will use net IDs from this list.		*/
/*----------------------------------------------------------------------*/

Genericlist *break_up_bus(labelptr blab, objinstptr thisinst, Genericlist *netlist)
{
   static Genericlist *subnets = NULL;
   char *tptr;
   buslist *sbus, *jbus;
   int bpos, istart, iend, tlen, i, j, netstart, matched;
   char *buspos, *busend, *busptr;

   if (pin_is_bus(blab, thisinst) == FALSE) return NULL;
   if (subnets == NULL) {
      /* This happens on the first pass only */
      subnets = (Genericlist *)malloc(sizeof(Genericlist));
      subnets->net.list = (buslist *)malloc(sizeof(buslist));
   }
   subnets->subnets = 0;

   tptr = textprint(blab->string, thisinst);
   tlen = strlen(tptr) + 1;
   buspos = strchr(tptr, areawin->buschar);

   /* The notation "(...)" with NO TEXT preceding the opening bus	*/
   /* delimiter, is assumed to represent a numerical pin range.  So	*/
   /* instead of generating labels, e.g., "(1)", "(2)", etc., we	*/
   /* generate	labels "1", "2", etc.					*/

   if (buspos == NULL) {
      Fprintf(stderr, "Error:  Bus specification has no start delimiter!\n");
      goto doneBus;
   }

   netstart = (netlist->subnets == 0) ? netlist->net.id : 0;

   bpos = (int)(buspos - tptr);
   busend = find_delimiter(buspos);

   if (busend == NULL) {
      Fprintf(stderr, "Error:  Bus specification has no end delimiter!\n");
      goto doneBus;
   }

   /* Find the range of each bus */

   matched = 0;
   istart = -1;
   for (busptr = buspos + 1; busptr < busend; busptr++) {
      if (sscanf(busptr, "%d", &iend) == 0) break;
      while ((*busptr != ':') && (*busptr != '-') && (*busptr != ',')
		&& (*busptr != *busend))
	 busptr++;
      if ((*busptr == ':') || (*busptr == '-')) 	/* numerical range */
	 istart = iend;
      else {
	 if (istart < 0) istart = iend;
	 i = istart;
	 while (1) {

	    /* Create a new list entry for this subnet number */

	    subnets->subnets++;
	    subnets->net.list = (buslist *)realloc(subnets->net.list,
			subnets->subnets * sizeof(buslist));

	    sbus = subnets->net.list + subnets->subnets - 1;
	    sbus->subnetid = i;
	    if (netstart > 0) {
	       sbus->netid = netstart++;
	       matched++;
	    }
	    else {
	       /* Net ID is the net ID for the matching subnet of netlist */
	       for (j = 0; j < netlist->subnets; j++) {
		  jbus = netlist->net.list + j;
		  if (jbus->subnetid == i) {
		     matched++;
		     sbus->netid = jbus->netid;
		     break;
		  }
	       }
	       /* Insert a net ID of zero if it can't be found */
	       if (j == netlist->subnets) {
		  sbus->netid = 0;
	       }
	    }

	    if (i == iend) break;
	    else if (istart > iend) i--;
	    else i++;
	 }
	 istart = -1;
      }
   }

doneBus:
   free(tptr);
   return (matched == 0) ? NULL : subnets;
}

/*----------------------------------------------------------------------*/
/* Test equivalence of two label strings (relaxed constraints)		*/
/*    Like stringcomp(), but ignores "superficial" differences such as  */
/*    color and font (unless one of the fonts is Symbol), scale,	*/
/*    underlining, tabbing, and kerning.				*/
/*									*/
/* Return 0 if matching.  Return 1 if not matching.			*/
/*									*/
/* For bus notation, ignore everything inside the bus delimiters.	*/
/* The calling routine must determine if the labels being compared	*/
/* have matching subnet ranges.  Note that as written, this does not	*/
/* check any text occurring after the opening bus delimiter!  Thus,	*/
/* "mynet(1:2)" and "mynet(3:4)" and "mynet(1)_alt" are all considered	*/
/* exact matches in bus notation.					*/
/*----------------------------------------------------------------------*/

int stringcomprelaxed(stringpart *string1, stringpart *string2,
			objinstptr thisinst)
{
   stringpart *strptr1 = string1, *strptr2 = string2;
   Boolean font1 = False, font2 = False, inbus_match = TRUE;
   int in_bus = 0;
   char *buspos;
   int bpos;

   if (strptr1->type == FONT_NAME)
      font1 = issymbolfont(strptr1->data.font);
   if (strptr2->type == FONT_NAME)
      font2 = issymbolfont(strptr2->data.font);

   while ((strptr1 != NULL) || (strptr2 != NULL)) {
      while (strptr1 != NULL && strptr1->type != TEXT_STRING &&
		strptr1->type != OVERLINE) {
	 if (strptr1->type == FONT_NAME)
	    font1 = issymbolfont(strptr1->data.font);
	 strptr1 = nextstringpart(strptr1, thisinst);
      }
      while (strptr2 != NULL && strptr2->type != TEXT_STRING &&
		strptr2->type != OVERLINE) {
	 if (strptr2->type == FONT_NAME)
	    font2 = issymbolfont(strptr2->data.font);
	 strptr2 = nextstringpart(strptr2, thisinst);
      }
      if (strptr1 == NULL || strptr2 == NULL) break;
      if (font1 != font2) return 1;
      if (strptr1->type != strptr2->type) return 1;
      else {
         switch (strptr1->type) {
	    case TEXT_STRING:
	       if (in_bus == 1) {
		  char matchchar = areawin->buschar;
		  switch (areawin->buschar) {
		     case '(': matchchar = ')'; break;
		     case '[': matchchar = ']'; break;
		     case '{': matchchar = '}'; break;
		     case '<': matchchar = '>'; break;
		  }
		  buspos = strchr(strptr1->data.string, matchchar);
		  if (buspos != NULL) {
		     bpos = (int)(buspos - (char *)(strptr1->data.string));
		     if (strlen(strptr2->data.string) > bpos) {
		        if (!strcmp(strptr1->data.string + bpos,
			  	strptr2->data.string + bpos)) {
		           in_bus = 2;
		           break;
			}
		     }
		     return 1;
		  }
		  if (inbus_match == TRUE)
		     if (strcmp(strptr1->data.string, strptr2->data.string))
			 inbus_match = FALSE;
	       }
	       else if (!strcmp(strptr1->data.string, strptr2->data.string))
		  break;

	       /* To be a matching bus, the strings match everywhere	*/
	       /* except between the bus notation delimiters (default	*/
	       /* "()".							*/
		
	       buspos = strchr(strptr1->data.string, areawin->buschar);
	       if (buspos != NULL) {

		  bpos = (int)(buspos - (char *)(strptr1->data.string)) + 1;
		  if (!strncmp(strptr1->data.string, strptr2->data.string, bpos)) {
		     in_bus = 1;
		     break;
		  }
	       }
	       return 1;  /* strings did not match, exactly or as bus notation */
	       break;
	    case OVERLINE:
	       if (strptr1->type != strptr2->type) return 1;
	       break;
         }
	 strptr1 = nextstringpart(strptr1, thisinst);
	 strptr2 = nextstringpart(strptr2, thisinst);
      }
   }

   /* One string continues after the other ends. . . */ 
   if (strptr1 != NULL || strptr2 != NULL) return 1;

   /* Treat no closing bus delimiter as a non-bus string */
   else if ((in_bus == 1) && (inbus_match == FALSE)) return 1;
   return 0;
}

/*----------------------------------------------------------------------*/
/* Find the number of parts in a string	(excluding parameter contents)	*/
/*----------------------------------------------------------------------*/

int stringparts(stringpart *string)
{
   stringpart *strptr;
   int ptotal = 0;

   for (strptr = string; strptr != NULL; strptr = strptr->nextpart)
      ptotal++;

   return ptotal;
}

/*----------------------------------------------------------------------*/
/* Compute the total character length of a string 			*/
/*    If "doparam" is True, include parameter contents.			*/
/*----------------------------------------------------------------------*/

int stringlength(stringpart *string, Boolean doparam, objinstptr thisinst)
{
   stringpart *strptr;
   int ctotal = 0;

   for (strptr = string; strptr != NULL; strptr = (doparam) ?
		nextstringpart(strptr, thisinst) : strptr->nextpart) {
      if (strptr->type == TEXT_STRING) {
	 if (strptr->data.string)
	    ctotal += strlen(strptr->data.string);
      }
      else
	 ctotal++;
   }

   return ctotal;
}

/*----------------------------------------------------------------------*/
/* Copy the contents of a string (excluding parameter contents)		*/
/*----------------------------------------------------------------------*/

stringpart *stringcopy(stringpart *string)
{
   stringpart *strptr, *newpart, *newtop = NULL, *topptr;

   for (strptr = string; strptr != NULL; strptr = strptr->nextpart) {

      /* Don't use makesegment(), which looks at parameter contents */
      newpart = (stringpart *)malloc(sizeof(stringpart));
      newpart->nextpart = NULL;
      if (newtop == NULL)
	 newtop = newpart;
      else 
	 topptr->nextpart = newpart;
      topptr = newpart;

      newpart->type = strptr->type;
      if ((strptr->type == TEXT_STRING) || (strptr->type == PARAM_START)) {
	 newpart->data.string = (char *)malloc(1 + strlen(strptr->data.string));
	 strcpy(newpart->data.string, strptr->data.string);
      }
      else
         newpart->data = strptr->data;
   }
   return newtop;
}

/*----------------------------------------------------------------------*/
/* Copy the contents of a string, embedding parameter contents		*/
/*----------------------------------------------------------------------*/

stringpart *stringcopyall(stringpart *string, objinstptr thisinst)
{
   stringpart *strptr, *newpart, *newtop, *topend;

   for (strptr = string; strptr != NULL;
		strptr = nextstringpart(strptr, thisinst)) {
      newpart = (stringpart *)malloc(sizeof(stringpart));
      newpart->type = strptr->type;
      newpart->nextpart = NULL;
      if (strptr == string) newtop = newpart;
      else topend->nextpart = newpart;
      topend = newpart;
      if ((strptr->type == TEXT_STRING || strptr->type == PARAM_START)
		&& strptr->data.string) {
	 newpart->data.string = (char *)malloc(1 + strlen(strptr->data.string));
	 strcpy(newpart->data.string, strptr->data.string);
      }
      else
         newpart->data = strptr->data;
   }
   return newtop;
}

/*----------------------------------------------------------------------*/
/* Copy the contents of a saved string with embedded parameter contents	*/
/* back to the string and the instance parameters.			*/
/*----------------------------------------------------------------------*/

stringpart *stringcopyback(stringpart *string, objinstptr thisinst)
{
   stringpart *strptr, *newpart, *curend = NULL;
   stringpart *rettop, *curtop, *savend = NULL;
   char *key = NULL;
   oparamptr pparam;
   Boolean need_free;

   for (strptr = string; strptr != NULL; strptr = strptr->nextpart) {

      newpart = (stringpart *)malloc(sizeof(stringpart));
      newpart->type = strptr->type;
      newpart->nextpart = NULL;
      newpart->data.string = NULL;

      if (strptr == string) rettop = newpart;	/* initial segment */
      else curend->nextpart = newpart;  	/* append segment to label */

      if (curend) {
         if (curend->type == PARAM_START) {
	    key = curend->data.string;
	    curtop = newpart;
	    savend = curend;
	    need_free = False;
         }
         else if (curend->type == PARAM_END) {
	    curend->nextpart = NULL;
	    savend->nextpart = newpart;
	    if (need_free) freelabel(curtop);
	    need_free = False;
         }
      }
      curend = newpart;

      if (strptr->type == TEXT_STRING || strptr->type == PARAM_START) {
	 if (strptr->data.string) {
	    newpart->data.string = (char *)malloc(1 + strlen(strptr->data.string));
	    strcpy(newpart->data.string, strptr->data.string);
	 }
	 else
	    newpart->data.string = NULL;
      }
      else if (strptr->type == PARAM_END) {
	 if (key != NULL) {
	    pparam = find_param(thisinst, key);
	    if (pparam == NULL) {
	       Fprintf(stderr, "Error:  Bad parameter %s encountered!\n", key);
	    }
	    else if (pparam->type == XC_STRING) {
	       freelabel(pparam->parameter.string);
	       pparam->parameter.string = curtop;
	       key = NULL;
	    }
	    else {
	       float fval;
	       int ival;
	       char *tmpstr = textprint(curtop, thisinst);

	       /* Promote string types into the type of the parameter */
	       switch (pparam->type) {
		  case XC_INT:
		     if (sscanf(tmpstr, "%d", &ival) == 1)
		        pparam->parameter.ivalue = ival;
		     free(tmpstr);
		     break;
		  case XC_FLOAT:
		     if (sscanf(tmpstr, "%g", &fval) == 1)
		        pparam->parameter.fvalue = fval;
		     break;
		  case XC_EXPR:
		     /* Expression results are derived and cannot be	*/
		     /* changed except by changing the expression	*/
		     /* itself.						*/
		     break;
	       }
	       free(tmpstr);
	       need_free = True;
	       key = NULL;
	    }
	 }
         else {
	    Fprintf(stderr, "Error:  Bad parameter in stringcopyback()\n");
	 }
      }
      else
         newpart->data = strptr->data;
   }

   /* tie up loose ends, if necessary */
   if ((curend != NULL) && (curend->type == PARAM_END)) {
      savend->nextpart = NULL;
      if (need_free) freelabel(curtop);
   }

   return rettop;
}

/*---------------------------------------------------------------------*/
/* draw a single character at 0, 0 using current transformation matrix */
/*---------------------------------------------------------------------*/

short UDrawChar(u_char code, short styles, short ffont, int groupheight,
	int passcolor, float passwidth)
{
   objectptr drawchar;
   XPoint alphapts[2];
   short  localwidth;
   objinst charinst;

   if ((ffont >= fontcount) || (fonts[ffont].encoding == NULL))
      return 0;

   alphapts[0].x = 0;
   alphapts[0].y = 0;
   charinst.type = OBJINST;
   charinst.color = DEFAULTCOLOR;
   charinst.rotation = 0;
   charinst.scale = fonts[ffont].scale;
   charinst.position = alphapts[0];
   charinst.params = NULL;
   
   /* get proper font and character */

   drawchar = fonts[ffont].encoding[(u_char)code];
   charinst.thisobject = drawchar;

   localwidth = (drawchar->bbox.lowerleft.x + drawchar->bbox.width) * fonts[ffont].scale;

   if ((fonts[ffont].flags & 0x22) == 0x22) { /* font is derived and italic */
      USlantCTM(DCTM, 0.25);  		/* premultiply by slanting function */
   }

   if (!(styles & 64)) {
      
      UDrawObject(&charinst, SINGLE, passcolor, passwidth, NULL);

      /* under- and overlines */
      if (styles & 8)
         alphapts[0].y = alphapts[1].y = -6;
      else if (styles & 16)
         alphapts[0].y = alphapts[1].y = groupheight + 4;
      if (styles & 24) {
         alphapts[0].x = 0; alphapts[1].x = localwidth;
         UDrawSimpleLine(&alphapts[0], &alphapts[1]);
      }
   }
   return localwidth;
}

/*----------------------------------------------------------------------*/
/* Draw an entire string, including parameter substitutions		*/
/* (Normally called as UDrawString(); see below)			*/
/*----------------------------------------------------------------------*/

void UDrawString0(labelptr drawlabel, int passcolor, objinstptr localinst,
	Boolean drawX)
{
   stringpart *strptr;
   char *textptr;
   short  fstyle, ffont, tmpjust, baseline;
   int    pos, group = 0;
   int    defaultcolor, curcolor, scolor;
   short  oldx, oldfont, oldstyle;
   float  tmpscale = 1.0, natscale = 1.0, tmpthick = 2.0;
   XPoint newpoint, bboxin[2], bboxout[2];
   u_char xm, ym;
   TextExtents tmpext;
   short *tabstops = NULL;
   short tabno, numtabs = 0;
   int   marginstop = 0;

   if (fontcount == 0) return;

   /* Don't draw temporary labels from schematic capture system */
   if (drawlabel->string->type != FONT_NAME) return;

   if (passcolor == DOSUBSTRING)
      defaultcolor = curcolor = drawlabel->color;
   else
      defaultcolor = curcolor = passcolor;

   if (defaultcolor != DOFORALL) {
      if (drawlabel->color != DEFAULTCOLOR)
	 curcolor = drawlabel->color;
      else
	 curcolor = defaultcolor;
      XTopSetForeground(curcolor);
   }

   /* calculate the transformation matrix for this object */
   /* in natural units of the alphabet vectors		  */
   /* (conversion to window units)			  */

   UPushCTM();
   UPreMultCTM(DCTM, drawlabel->position, drawlabel->scale, drawlabel->rotation);

   /* check for flip invariance; recompute CTM and justification if necessary */

   tmpjust = flipadjust(drawlabel->justify);

   /* "natural" (unscaled) length */
   tmpext = ULength(drawlabel, localinst, 0, NULL);

   newpoint.x = (tmpjust & NOTLEFT ?
       (tmpjust & RIGHT ? -tmpext.maxwidth : -tmpext.maxwidth >> 1) : 0);
   newpoint.y = (tmpjust & NOTBOTTOM ?
       (tmpjust & TOP ? -tmpext.ascent : -(tmpext.ascent + tmpext.base) >> 1)
		: -tmpext.base);

   /* Pinlabels have an additional offset spacing to pad */
   /* them from the circuit point to which they attach.  */

   if (drawlabel->pin) {
      pinadjust(tmpjust, &(newpoint.x), &(newpoint.y), 1);
   }

   oldx = newpoint.x;
   baseline = newpoint.y;

   /* do quick calculation on bounding box; don't draw if off-screen */

   bboxin[0].x = newpoint.x;
   bboxin[0].y = newpoint.y + tmpext.descent;
   bboxin[1].x = newpoint.x + tmpext.width;
   bboxin[1].y = newpoint.y + tmpext.ascent;
   UTransformbyCTM(DCTM, bboxin, bboxout, 2);
   xm = (bboxout[0].x < bboxout[1].x) ? 0 : 1;
   ym = (bboxout[0].y < bboxout[1].y) ? 0 : 1;

   if (bboxout[xm].x < areawin->width && bboxout[ym].y < areawin->height &&
       bboxout[1 - xm].x > 0 && bboxout[1 - ym].y > 0) {

       pos = 0;
       for (strptr = drawlabel->string; strptr != NULL;
		strptr = nextstringpart(strptr, localinst)) {

	  /* All segments other than text cancel any	*/
	  /* existing overline/underline in effect.	*/

	  if (strptr->type != TEXT_STRING)
	     fstyle &= 0xfc7;

          /* deal with each text segment type */

	  switch(strptr->type) {
	     case FONT_NAME:
		if (strptr->data.font < fontcount) {
		   ffont = strptr->data.font;
		   fstyle = 0;		   /* style reset by font change */
	           if (baseline == newpoint.y) {  /* set top-level font and style */
	              oldfont = ffont;
	              oldstyle = fstyle;
	           }
		}
		
		/* simple boldface technique for derived fonts */

		tmpthick = ((fonts[ffont].flags & 0x21) == 0x21) ?  4.0 : 2.0;
		break;

	     case FONT_SCALE:
		tmpscale = natscale * strptr->data.scale;
	        if (baseline == newpoint.y) /* reset top-level scale */
		   natscale = tmpscale;
		break;

	     case KERN:
	        newpoint.x += strptr->data.kern[0];
	        newpoint.y += strptr->data.kern[1];
		break;
		
	     case FONT_COLOR:
		if (defaultcolor != DOFORALL) {
		   if (strptr->data.color != DEFAULTCOLOR)
		      curcolor = colorlist[strptr->data.color].color.pixel;
		   else {
		      if (curcolor != DEFAULTCOLOR) {
			 XTopSetForeground(defaultcolor);
		      }
		      curcolor = DEFAULTCOLOR;
		   }
		}
		break;

	     case TABBACKWARD:	/* find first tab value with x < xtotal */
	        for (tabno = numtabs - 1; tabno >= 0; tabno--) {
	           if (tabstops[tabno] < newpoint.x) {
		      newpoint.x = tabstops[tabno];
		      break;
	           }
	        }
	        break;

	     case TABFORWARD:	/* find first tab value with x > xtotal */
	        for (tabno = 0; tabno < numtabs; tabno++) {
	           if (tabstops[tabno] > newpoint.x) {
		      newpoint.x = tabstops[tabno];
		      break;
	           }
	        }
	        break;

	     case TABSTOP:
	        numtabs++;
	        if (tabstops == NULL) tabstops = (short *)malloc(sizeof(short));
	        else tabstops = (short *)realloc(tabstops, numtabs * sizeof(short));
	        tabstops[numtabs - 1] = newpoint.x;
		break;

	     case MARGINSTOP:
	     case RETURN:
		tmpscale = natscale = 1.0;
		baseline -= BASELINE;
	        newpoint.y = baseline;
		newpoint.x = oldx;
		break;
	
	     case SUBSCRIPT:
	        natscale *= SUBSCALE; 
		tmpscale = natscale;
	        newpoint.y -= (short)((TEXTHEIGHT >> 1) * natscale);
		break;

	     case SUPERSCRIPT:
	        natscale *= SUBSCALE;
		tmpscale = natscale;
	        newpoint.y += (short)(TEXTHEIGHT * natscale);
		break;

	     case NORMALSCRIPT:
	        tmpscale = natscale = 1.0;
	        ffont = oldfont;	/* revert to top-level font and style */
	        fstyle = oldstyle;
	        newpoint.y = baseline;
		break;

	     case UNDERLINE:
	        fstyle |= 8;
		break;

	     case OVERLINE:
		if (strptr->nextpart != NULL && strptr->nextpart->type == TEXT_STRING) {
		   objectptr charptr;
		   int tmpheight;

		   group = 0;
		   for (textptr = strptr->nextpart->data.string;
				textptr && *textptr != '\0'; textptr++) {
		      charptr = fonts[ffont].encoding[*(u_char *)textptr];
		      tmpheight = (int)((float)charptr->bbox.height
				* fonts[ffont].scale);
		      if (group < tmpheight) group = tmpheight;
		   }
	           fstyle |= 16;
		}
		break;

	     case NOLINE:
		break;

	     case HALFSPACE: case QTRSPACE: {
		short addx;
		UPushCTM();
		UPreMultCTM(DCTM, newpoint, tmpscale, 0);
		addx = UDrawChar((u_char)32, fstyle, ffont, group,
			curcolor, tmpthick);
		newpoint.x += addx >> ((strptr->type == HALFSPACE) ? 1 : 2);
		UPopCTM();
		} break;

	     case TEXT_STRING:
		textptr = strptr->data.string;

		/* Don't write technology names in catalog mode if this	*/
		/* option is enabled	(but *not* CATTEXT_MODE!)	*/

		if (((eventmode == CATALOG_MODE) && !xobjs.showtech)
			|| ((eventmode == CATTEXT_MODE)
			&& (drawlabel != TOLABEL(EDITPART)))) {
		   char *nsptr = strstr(textptr, "::");
		   if (nsptr != NULL) {
		      textptr = nsptr + 2;
		      pos += (pointertype)nsptr - (pointertype)strptr->data.string + 2;
		   }
		}

		for (; textptr && *textptr != '\0'; textptr++) {
		   pos++;
		   UPushCTM();
		   UPreMultCTM(DCTM, newpoint, tmpscale, 0);

	           /* Special case of selection:  only substring is	*/
		   /* drawn in the selection color.			*/

		   scolor = curcolor;
	           if (passcolor == DOSUBSTRING) {
	              if (pos <= areawin->textpos && pos > areawin->textend)
		         scolor = SELECTCOLOR;
		      else if (pos > areawin->textpos) {
      		         XTopSetForeground(curcolor);
		      }
	           }
	           newpoint.x += UDrawChar(*textptr, fstyle, ffont,
			group, scolor, tmpthick) * tmpscale;

		   UPopCTM();
		}
		pos--;
		break;
	  }
	  pos++;
       }
   }

   /* enddraw: (jdk) */

   if (tabstops != NULL) free(tabstops);

   /* Pop the string transformation matrix */

   UPopCTM();

   if (drawX && drawlabel->pin) UDrawXDown(drawlabel);

   if ((defaultcolor != DOFORALL) && (passcolor != curcolor)) {
      XTopSetForeground(passcolor);
   }
}

/*----------------------------------------------------------------------*/
/* Draw String, with an "x" mark at the origin				*/
/*----------------------------------------------------------------------*/

void UDrawString(labelptr drawlabel, int passcolor, objinstptr localinst)
{
   UDrawString0(drawlabel, passcolor, localinst, TRUE);
}

/*----------------------------------------------------------------------*/
/* Draw String, without the "x" mark					*/
/*----------------------------------------------------------------------*/

void UDrawStringNoX(labelptr drawlabel, int passcolor, objinstptr localinst)
{
   UDrawString0(drawlabel, passcolor, localinst, FALSE);
}

/*----------------------------------------------------------------------*/
/* Compute the actual length of a string or portion thereof.		*/
/*----------------------------------------------------------------------*/

TextExtents ULength(labelptr drawlabel, objinstptr localinst,
	short dostop, XPoint *tbreak)
{
   float oldscale, strscale, natscale, locscale = 1.0, xtotal = 0.5;
   float lasttotal = xtotal;
   stringpart *strptr;
   u_char *textptr;
   objectptr *somebet = NULL, chptr;
   short locpos = 0, lastpos = 0;
   float ykern = 0.0;
   TextExtents retext;
   short *tabstops = NULL;
   short tabno, numtabs = 0;
   int marginstop = 0;

   retext.ascent = retext.descent = retext.base = 0;
   retext.width = retext.maxwidth = 0;

   if (fontcount == 0) return retext;

   /* Don't draw temporary labels from schematic capture system */
   else if (drawlabel->string->type != FONT_NAME) return retext;

   natscale = 1.0;
     
   oldscale = strscale = natscale;

   for (strptr = drawlabel->string; strptr != NULL;
		strptr = nextstringpart(strptr, localinst)) {
      switch (strptr->type) {
	 case SUPERSCRIPT:
	    natscale *= SUBSCALE;
	    strscale = natscale;
	    ykern += TEXTHEIGHT * natscale;
	    break;
	 case SUBSCRIPT:
	    natscale *= SUBSCALE;
	    strscale = natscale;
	    ykern -= TEXTHEIGHT * natscale / 2.0;
	    break;
	 case NORMALSCRIPT:
	    natscale = strscale = oldscale;
	    ykern = 0.0;
	    break;
	 case MARGINSTOP:
	 case RETURN:
	    natscale = strscale = oldscale;
	    ykern = 0.0;
	    retext.base -= BASELINE;
	    retext.maxwidth = max(retext.width, xtotal);
	    xtotal = 0.5;
	    break;
	 case HALFSPACE: 
	    if (somebet) {
	       chptr = (*(somebet + 32));
	       xtotal += (float)(chptr->bbox.width + chptr->bbox.lowerleft.x)
			* locscale * natscale / 2;
	    }
	    break;
	 case QTRSPACE:
	    if (somebet) {
	       chptr = (*(somebet + 32));
	       xtotal += (float)(chptr->bbox.width + chptr->bbox.lowerleft.x) 
			* locscale * natscale / 4;
	    }
	    break;
	 case TABBACKWARD:	/* find first tab value with x < xtotal */
	    for (tabno = numtabs - 1; tabno >= 0; tabno--) {
	       if (tabstops[tabno] < xtotal) {
		  xtotal = tabstops[tabno];
		  break;
	       }
	    }
	    break;
	 case TABFORWARD:	/* find first tab value with x > xtotal */
	    for (tabno = 0; tabno < numtabs; tabno++) {
	       if (tabstops[tabno] > xtotal) {
		  xtotal = tabstops[tabno];
		  break;
	       }
	    }
	    break;
	 case TABSTOP:
	    numtabs++;
	    if (tabstops == NULL) tabstops = (short *)malloc(sizeof(short));
	    else tabstops = (short *)realloc(tabstops, numtabs * sizeof(short));
	    tabstops[numtabs - 1] = xtotal;
	    break;
	 case FONT_SCALE:
	    strscale = natscale * strptr->data.scale;
	    if (ykern == 0.0)
	       natscale = strscale;
	    break;
	 case KERN:
	    xtotal += strptr->data.kern[0];
	    ykern += strptr->data.kern[1];
	    break;
	 case FONT_NAME:
	    if (strptr->data.font < fontcount) {
	       somebet = fonts[strptr->data.font].encoding;
	       locscale = fonts[strptr->data.font].scale;
	       if (ykern == 0.0)
	          natscale = locscale;
	    }
	    break;
	 case TEXT_STRING:
	    textptr = strptr->data.string;

	    /* Don't write technology names in catalog mode if	*/
	    /* the option is enabled, so ignore when measuring	*/

	    if (((eventmode == CATALOG_MODE) && !xobjs.showtech)
			|| ((eventmode == CATTEXT_MODE)
			&& (drawlabel != TOLABEL(EDITPART)))) {
		char *nsptr = strstr(textptr, "::");
		if (nsptr != NULL) {
		   textptr = nsptr + 2;
		   locpos += (pointertype)nsptr - (pointertype)strptr->data.string + 2;
		}
	    }

	    if (somebet == NULL) break;

	    for (; textptr && *textptr != '\0'; textptr++) {
               if (dostop && (locpos >= dostop)) break;
	       locpos++;

	       chptr = (*(somebet + *textptr));
	       xtotal += (float)(chptr->bbox.width + chptr->bbox.lowerleft.x)
			* locscale * strscale;
	       retext.ascent = max(retext.ascent, (short)(retext.base + ykern +
			(float)((chptr->bbox.height + chptr->bbox.lowerleft.y)
			* locscale * strscale)));
	       retext.descent = min(retext.descent, (short)(retext.base + ykern +
			(float)(chptr->bbox.lowerleft.y * locscale * strscale)));

               if (tbreak != NULL) 
	          if ((xtotal > tbreak->x) && (retext.base <= tbreak->y)) break;
               lasttotal = xtotal;
	       lastpos = locpos;
	    }
	    break;
      }
      if (strptr->type != TEXT_STRING) locpos++;
      if (dostop && (locpos >= dostop)) break;
   }
   if (tabstops != NULL) free(tabstops);

   /* special case: return character position in retext.width */
   if (tbreak != NULL) {
      int slen = stringlength(drawlabel->string, True, localinst);
      if ((tbreak->x - lasttotal) < (xtotal - tbreak->x))
	 locpos = lastpos + 1;
      if (locpos < 1) locpos = 1;
      else if (locpos > slen) locpos = slen;
      retext.width = locpos;
      return retext;
   }
   retext.width = max(retext.width, xtotal);
   retext.maxwidth = max(retext.maxwidth, xtotal);
   return retext;
}

/*----------------------------------------------------------------------*/
/* Remove all RETURN directives following a MARGINSTOP.  Automatically	*/
/* generated line breaks are identified by an nonzero "flags" field.	*/
/*----------------------------------------------------------------------*/

void RemoveMarginNewlines(labelptr settext, objinstptr localinst)
{
   stringpart *strptr, *nextptr;
   int strpos = 0;

   for (strptr = settext->string; strptr != NULL;
		strptr = nextstringpart(strptr, localinst)) {
      switch (strptr->type) {
	 case RETURN:
	    if (strptr->data.flags != 0) {
	       // Remove
	       strptr = deletestring(strptr, &settext->string, localinst);
	       if (strpos <= areawin->textpos) areawin->textpos--;
	    }
	    else strpos++;
	    break;

	 case TEXT_STRING:
	    if (strptr->data.string)
	       strpos += strlen(strptr->data.string);
	    break;

	 default:
	    strpos++;
	    break;
      }
   }
}

/*----------------------------------------------------------------------*/
/* Analyze a text label and insert RETURN directives as necessary to	*/
/* keep the text within the width limit set by MARGIN.  Break up text	*/
/* at word boundaries where necessary.  This routine is run only when	*/
/* (1) editing a text label or loading one from a file, and (2) the	*/
/* text label both contains a MARGIN directive and exceeds the margin	*/
/* width, as determined by CheckMarginStop().  				*/
/*----------------------------------------------------------------------*/

void InsertMarginNewlines(labelptr settext, objinstptr localinst)
{
   stringpart *strptr;
   int margin = 0;
   int strpos = 0, locpos, tmplen, slen;
   TextExtents tmpext;

   /* 1) Find the position of the margin stop.  Track position	*/
   /* in string a la findstringpart(), as we need to pass this	*/
   /* to ULength()						*/

   for (strptr = settext->string; strptr != NULL;
		strptr = nextstringpart(strptr, localinst)) {
      switch (strptr->type) {
	 case MARGINSTOP:
	    margin = strptr->data.width;
	    strpos++;
	    break;

	 case TEXT_STRING:
	    if (strptr->data.string)
	       strpos += strlen(strptr->data.string);
	    break;

	 default:
	    strpos++;
	    break;
      }
      if (margin > 0) break;
   }
   if (margin == 0) return;	// Should not happen. . .

   /* 2) Compute the drawn string length at each word break.  When a	*/
   /*    word overruns the margin, place a line break in front of it.	*/

   while (1) {
      strptr = findstringpart(strpos, &locpos, settext->string, localinst);
      if (strptr == NULL) break;
      else if (strptr->type == TEXT_STRING) {
	 slen = strlen(strptr->data.string);
	 /* Ignore trailing spaces */
	 while ((slen > 0) && (*(strptr->data.string + slen - 1) == ' ')) slen--;
         tmpext = ULength(settext, localinst, strpos + slen, NULL);
	 if (tmpext.maxwidth > margin) {
            while ((slen > 0) && (tmpext.maxwidth > margin)) {
	       while ((slen > 0) && (*(strptr->data.string + slen - 1) != ' ')) slen--;
	       while ((slen > 0) && (*(strptr->data.string + slen - 1) == ' ')) slen--;
	       tmpext = ULength(settext, localinst, strpos + slen - 1, NULL);
	    }
	    if (slen > 0) {
	       // Split string at word separation before the margin
	       while ((slen > 0) && (*(strptr->data.string + slen) == ' ')) slen++;
	       strptr = splitstring(strpos + slen, &settext->string, localinst);
	       strptr = nextstringpart(strptr, localinst);
	    }
	    // Insert a carriage return
	    strptr = makesegment(&settext->string, strptr);
	    strptr->type = RETURN;
	    strptr->data.flags = 1;	/* Mark as auto-generated line wrap */
	    if (areawin->textpos > strpos) areawin->textpos++;
	    strpos += slen;
	 }
	 else
	    strpos += strlen(strptr->data.string);
      }
      else
         strpos++;
   }
}

/*----------------------------------------------------------------------*/
/* Check a string for presence of a MARGINSTOP directive.  If it has	*/
/* one, check if ULength exceeds the margin.  If so, remove all Return	*/
/* directives after the MARGINSTOP, and re-insert them such that the	*/
/* text stays within the margin.					*/
/*----------------------------------------------------------------------*/

void CheckMarginStop(labelptr settext, objinstptr localinst, Boolean force)
{
   stringpart *strptr;
   int margin = 0;
   TextExtents tmpext;

   for (strptr = settext->string; strptr != NULL;
		strptr = nextstringpart(strptr, localinst)) {
      switch (strptr->type) {
	 case MARGINSTOP:
	    margin = strptr->data.width;
	    break;
      }
      if (margin > 0) break;
   }
   if (margin > 0) {
      tmpext = ULength(settext, localinst, 0, NULL);
      if ((force == TRUE) || (tmpext.maxwidth > margin)) {
	 RemoveMarginNewlines(settext, localinst);
	 InsertMarginNewlines(settext, localinst);
      }
   }
}

/*----------------------------------------------------------------------*/
/* low-level routines for drawing and erasing labels			*/
/*----------------------------------------------------------------------*/

void undrawtextsimple(labelptr settext)
{
   SetFunction(dpy, areawin->gc, GXcopy);
   XTopSetForeground(BACKGROUND);
   UDrawString(settext, DOFORALL, areawin->topinstance);
}

/*----------------------------------------------------------------------*/

void redrawtextsimple(labelptr settext)
{
   UDrawString(settext, settext->color, areawin->topinstance);
}

/*----------------------------------------------------------------------*/
/* Redraw all labels in the current object which contain the same	*/
/* parameter(s) as the indicated label.					*/
/* (It's easier not to bother to check for the same parameter, as there	*/
/* are typically so few parameters in an object that the extra compute	*/
/* and draw time is negligible.)					*/
/*									*/
/* Function pointer (undrawtextsimple or redrawtextsimple) indicates	*/
/* which function to call on this text label.				*/
/*----------------------------------------------------------------------*/

void drawtextandupdate(labelptr curlabel, void (*function)(labelptr))
{
   genericptr *pgen;
   labelptr slab;

   for (pgen = topobject->plist; pgen < topobject->plist + topobject->parts;
		pgen++) {
      if (IS_LABEL(*pgen)) {
	 slab = TOLABEL(pgen);
	 if (slab == curlabel) continue;
	 if (hasparameter(slab))
	    function(slab);
      }
   }
}

/*----------------------------------------------------------------------*/
/* Wrapper functions for drawtextandupdate()				*/
/*----------------------------------------------------------------------*/

void undrawtext(labelptr curlabel)
{
   undrawtextsimple(curlabel);

   if (hasparameter(curlabel))
      drawtextandupdate(curlabel, undrawtextsimple);
}

/*----------------------------------------------------------------------*/

void redrawtext(labelptr curlabel)
{
   redrawtextsimple(curlabel);

   if (hasparameter(curlabel))
      drawtextandupdate(curlabel, redrawtextsimple);
}

/*----------------------------------------------------------------------*/
/* Draw the catalog of font characters 					*/
/*----------------------------------------------------------------------*/

void composefontlib(short cfont)
{
  /* genericptr *pgen; (jdk) */
   objinstptr *drawinst;
   objectptr *curlib, libobj, nullobj;
   objectptr directory = xobjs.libtop[FONTLIB]->thisobject;
   short visobjects, i, qdel;
   polyptr *drawbox;
   pointlist pointptr;

   reset(directory, NORMAL);

   /* Create a pointer to the font library */

   curlib = xobjs.fontlib.library;

   /* Find the number of non-null characters.  Do this by assuming */
   /* that all fonts encode nullchar at position zero.		   */

   visobjects = 0;
   nullobj = fonts[cfont].encoding[0];
   for(i = 1; i < 256; i++)
      if (fonts[cfont].encoding[i] != nullobj) visobjects++;

   /* add the box and gridlines */

   visobjects += 34;

   /* generate the list of object instances */

   directory->plist = (genericptr *) realloc(directory->plist, visobjects
		* sizeof(genericptr));
   directory->parts = 0;

   /* 0.5 is the default vscale;  16 is no. characters per line */
   del = min(areawin->width, areawin->height) / (0.5 * 16);
   qdel = del >> 2;

   for (i = 0; i < 256; i++) {

      if ((libobj = fonts[cfont].encoding[i]) == nullobj) continue;
      
      NEW_OBJINST(drawinst, directory);
      instancedefaults(*drawinst, libobj,
		(i % 16) * del + qdel,		/* X position */
		-(i / 16) * del + qdel);	/* Y position */
      drawinst = (objinstptr *)directory->plist + directory->parts - 1;
      (*drawinst)->color = DEFAULTCOLOR;
   }

   /* separate characters with gridlines (17 vert., 17 horiz.) */

   for (i = 0; i < 34; i++) {
      NEW_POLY(drawbox, directory);
      polydefaults(*drawbox, 2, 0, 0);

      (*drawbox)->color = SNAPCOLOR;   /* default red */
      (*drawbox)->style = UNCLOSED;
      (*drawbox)->width = 1.0;

      if (i < 17) {
         pointptr = (*drawbox)->points;
         pointptr->x = i * del;
         pointptr->y = 0;
         pointptr = (*drawbox)->points + 1;
         pointptr->x = i * del;
         pointptr->y = -16 * del;
      }
      else {
         pointptr = (*drawbox)->points;
         pointptr->x = 0;
         pointptr->y = (17 - i) * del;
         pointptr = (*drawbox)->points + 1;
         pointptr->x = 16 * del;
         pointptr->y = (17 - i) * del;
      }
   }

   /* Set the bounding box for this display. 				*/
   /* This is just the bounds of the grid built above, so there's no	*/
   /* need to call any of the bounding box calculation routines.     	*/

   directory->bbox.lowerleft.x = 0;
   directory->bbox.lowerleft.y = pointptr->y;
   directory->bbox.width = pointptr->x;
   directory->bbox.height = pointptr->x;

   xobjs.libtop[FONTLIB]->bbox.lowerleft.x = 0;
   xobjs.libtop[FONTLIB]->bbox.lowerleft.y = pointptr->y;
   xobjs.libtop[FONTLIB]->bbox.width = pointptr->x;
   xobjs.libtop[FONTLIB]->bbox.height = pointptr->x;

   centerview(xobjs.libtop[FONTLIB]);
}

/*------------------------------------------------------*/
/* ButtonPress handler during font catalog viewing mode */
/*------------------------------------------------------*/

void fontcat_op(int op, int x, int y)
{
   short chx, chy;
   u_long rch = 0;

   if (op != XCF_Cancel) {

      window_to_user(x, y, &areawin->save);
 
      chy = -areawin->save.y / del + 1;
      chx = areawin->save.x / del;

      chx = min(15, chx);
      chy = min(15, chy);
    
      rch = (u_long)(chy * 16 + chx);
   }

   catreturn();

   if (rch != 0)
      labeltext(rch, NULL);
}

/*-------------------------------------------------------------------------*/
