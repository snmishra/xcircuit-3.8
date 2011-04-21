/*-------------------------------------------------------------------------*/
/* colordefs.h 								   */
/* Copyright (c) 2002  Tim Edwards, Johns Hopkins University       	   */
/*-------------------------------------------------------------------------*/

/*-------------------------------------------------------------------------*/
/* Add colors here as needed. 						   */
/* Reflect all changes in the resource manager, xcircuit.c		   */
/* And ApplicationDataPtr in xcircuit.h					   */
/*-------------------------------------------------------------------------*/

#define NUMBER_OF_COLORS	17

#define BACKGROUND	appcolors[0]
#define FOREGROUND	appcolors[1]
#define SELECTCOLOR     appcolors[2]
#define FILTERCOLOR	appcolors[3] 
#define GRIDCOLOR	appcolors[4]
#define SNAPCOLOR	appcolors[5]
#define AXESCOLOR	appcolors[6]
#define OFFBUTTONCOLOR	appcolors[7]
#define AUXCOLOR	appcolors[8]
#define BARCOLOR	appcolors[9]
#define PARAMCOLOR	appcolors[10]

/* The rest of the colors are layout colors, not GUI colors */

#define BBOXCOLOR	appcolors[11]
#define LOCALPINCOLOR	appcolors[12]
#define GLOBALPINCOLOR	appcolors[13]
#define INFOLABELCOLOR	appcolors[14]
#define RATSNESTCOLOR	appcolors[15]
#define CLIPMASKCOLOR	appcolors[15]

#define DEFAULTCOLOR	-1		/* Inherits color of parent */
#define DOFORALL	-2		/* All elements inherit same color */
#define DOSUBSTRING	-3		/* Only selected substring drawn */
					/* in the SELECTCOLOR		*/
#define BADCOLOR	-1		/* When returned from query_named_color */
#define ERRORCOLOR	-2		/* When returned from query_named_color */

/*-------------------------------------------------------------------------*/
