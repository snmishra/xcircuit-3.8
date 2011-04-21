/************************************************************
**
**       COPYRIGHT (C) 1993 UNIVERSITY OF PITTSBURGH
**       COPYRIGHT (C) 1996 GANNON UNIVERSITY
**                  ALL RIGHTS RESERVED
**
**        This software is distributed on an as-is basis
**        with no warranty implied or intended.  No author
**        or distributor takes responsibility to anyone 
**        regarding its use of or suitability.
**
**        The software may be distributed and modified 
**        freely for academic and other non-commercial
**        use but may NOT be utilized or included in whole
**        or part within any commercial product.
**
**        This copyright notice must remain on all copies 
**        and modified versions of this software.
**
************************************************************/


/* file parse.c */
/* ------------------------------------------------------------------------
 * IVF parser routines. these should track the ones in 
 * the vhdl code. see the include stuff below.
 * ------------------------------------------------------------------------
 */
#include <stdio.h>
#include <stdarg.h>
#include <ctype.h>
#include <string.h>


/* for compatibility with the rest of the Keystone VHDL system */
#include "system_defs.h"
#include "ivf_format.h"
#include "net.h"
#include "externs.h"
/*---------------------------------------------------------------
 * Forward References
 *---------------------------------------------------------------
 */
char *find_token();
char *get_next_token();
void ivf_sig_def();
void ivf_gate_def();
void ivf_proc_def();


/*---------------------------------------------------------------
 * Global Variable Definitions
 *---------------------------------------------------------------
 */

static FILE *in_file;
module *curobj_module;

/*---------------------------------------------------------------
 * utility definition from presim.c
 *---------------------------------------------------------------
 */

#define CHK_IVF_END(a) \
     if ((a) == NULL) \
        { \
          fprintf (stderr, "premature end to .ivf file found\n"); \
          exit (1); \
        }

/*---------------------------------------------------------------
 * read_ivf parse .ivf file (code from vhdl/vsim/presim.c)
 *---------------------------------------------------------------
 */

read_ivf (in)
    FILE           *in;
{
    char           *tok_ptr;
    char	signame[128], sigdir[32];
    char	busname[128];
    int 	high, low;
    

    in_file = in;

    /* before we start add the predefined constant signals 
     * $0 $1, and _DUMMY_SIGNAL_
     */
  newnode("$0");
    newnode("$1");
    newnode("_DUMMY_SIGNAL_");
    
    /* we pick up the external port info from the hierarchy view */

    tok_ptr = find_token (MOD_START_EXP);
    CHK_IVF_END (tok_ptr);

    tok_ptr = find_token (MOD_PORT);
    CHK_IVF_END (tok_ptr);

    tok_ptr = find_token(IVF_OPEN_STR);
    CHK_IVF_END (tok_ptr);

    tok_ptr = get_next_token();
    CHK_IVF_END (tok_ptr);

/* This code counts too much on the format of ivf files.
 * We assume triples of: "signame" "sigdir" ";" including a ";" at the 
 * end, before the closing brace.
 */
    while (strcmp(tok_ptr, IVF_CLOSE_STR))
    {
	strcpy(signame, tok_ptr);

	tok_ptr = get_next_token();
	CHK_IVF_END (tok_ptr);
	strcpy(sigdir, tok_ptr);

	tok_ptr = get_next_token();
	CHK_IVF_END (tok_ptr);

	/* check for array/bitvec busses */
	if(! strchr(signame, '['))
	{
	    add_port(signame, sigdir);
	}
	else /* we have a bitvec */
	{
	    sscanf(signame, "%[^[][ %d : %d ]", busname, &high, &low);
	    if(low <= high)
	    {
		for(; low <= high; low++)
		{
		    sprintf(signame, "%s_%d", busname, low);
		    add_port(signame, sigdir);
		}
	    }
	    else 
	    {
		error("bad bus spec in MP line of ivf file","");
	    }
	    
	        
	}
	
	tok_ptr = get_next_token();
	CHK_IVF_END (tok_ptr);

    }
    
    /* search for the flattened view  */
    tok_ptr = find_token (MOD_VIEW_FLAT);

    if (tok_ptr == NULL)
    {
	fprintf (stderr, "error, flattened description not found in .ivf file\n");
	exit (1);
    }

    tok_ptr = get_next_token ();

    if (strcmp (tok_ptr, IVF_OPEN_STR))
    {
	/* we couldn't find our open brace  */
	fprintf (stderr, "error, open brace not found in .ivf file\n");
	exit (1);
    }

    /* loop through the flattened view  */
    for (;;)
    {
	tok_ptr = get_next_token ();
	CHK_IVF_END (tok_ptr);

	if (!strcmp (tok_ptr, FLAT_SIG))
	{
	    /* definition of signals  */
	    ivf_sig_def ();
	}
	else if (!strcmp (tok_ptr, FLAT_GATE))
	{
	    /* primitive gate definition  */
	    ivf_gate_def ();
	}
	else if (!strcmp (tok_ptr, FLAT_PROC))
	{
	    /* process definition  */
	    ivf_proc_def ();
	}
	else if (!strcmp (tok_ptr, IVF_CLOSE_STR))
	{
	    /* our closeing brace, finis  */
	    break;
	}
	else
	{
	    /* error  */
	    fprintf (stderr, "illegal token, %s, found in flattened .ivf description",
		     tok_ptr);
	    exit (1);
	}
    }
}

/*---------------------------------------------------------------
 * from presim.c
 *---------------------------------------------------------------
 */

#define is_delimiter(a) (isspace((a)) || \
                         ((a) == IVF_OPEN_CHAR) || \
                         ((a) == IVF_CLOSE_CHAR)|| \
			 ((a) == ';'))
/* ADDED ';' which needs to be in ivf_format.h as
 * IVF_GATE_BAG_CHAR 
 */
/*---------------------------------------------------------------
 * from presim.c
 *---------------------------------------------------------------
 */

static char    *
get_next_token ()
{
    static char     line[LSIZE];
    int             done = FALSE;
    char           *c_ptr;

    c_ptr = &(line[0]);

    /* skip any white space  */
    do
    {
	if ((*c_ptr = getc (in_file)) == EOF)
	{
	    done = TRUE;
	    break;
	}

	if(*c_ptr == '\n') lcount++;
	
    }
    while (isspace (*c_ptr));

    if (done != TRUE)
    {
	/* save characters until we encounter a delimiter  */
	while (!is_delimiter (*c_ptr))
	{
	    ++c_ptr;

	    if ((*c_ptr = getc (in_file)) == EOF)
	    {
		done = TRUE;
		break;
	    }
	}

	/* advance the pointer if we don't have a white space delimiter  */
	if (!isspace (*c_ptr) && c_ptr == &(line[0]))
	{
	    c_ptr++;
	}
	else
	{
	    /* unget the delimiter  */
	    ungetc (*c_ptr, in_file);
	}

	/* nul-terminate the string  */
	*c_ptr = '\0';
    }

    if (done == TRUE)
    {
	/* we have reached EOF  */
	return (NULL);
    }
    else
    {
	return (&(line[0]));
    }
}

/*---------------------------------------------------------------
 * from presim.c
 *---------------------------------------------------------------
 */


static char    *
find_token (token_str)
    char           *token_str;
{
    char           *tok_ptr;
    char           *ret_val;

    for (;;)
    {
	tok_ptr = get_next_token ();

	/* if we've run out of input or found the token, we are done  */
	if (tok_ptr == NULL)
	{
	    ret_val = NULL;
	    break;
	}
	else if (!strcmp (token_str, tok_ptr))
	{
	    ret_val = tok_ptr;
	    break;
	}
    }

    return (ret_val);
}

/*---------------------------------------------------------------
 * from presim.c
 *---------------------------------------------------------------
 */

static void
ivf_sig_def ()
{
    char           *tok_ptr;

    /* verify we have our open brace  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    if (strcmp (tok_ptr, IVF_OPEN_STR))
    {
	fprintf (stderr, "found %s when expecting %s in .ivf file\n",
		 tok_ptr, IVF_OPEN_STR);
	exit (1);
    }

    for (;;)
    {
	tok_ptr = get_next_token ();
	CHK_IVF_END (tok_ptr);

	if (!strcmp (tok_ptr, IVF_CLOSE_STR))
	{
	    /* we found our terminating closing brace  */
	    break;
	}

	/* otherwise, add the specified signal to our string definitions  */
	newnode (tok_ptr);
    }
}

/*---------------------------------------------------------------
 * str_end_copy
 *---------------------------------------------------------------
 */

char *str_end_copy(new, old, n)
    char *new, *old;
    int n;
{
    /* Copy the last <n> characters from <old> to <new>. */
    int i, len = strlen(old);
    if (len > n)
    {
	strncpy(new, old, n);
	for (i=0; i<n; i++)
	{
	    new[i] = old[len-n+i];
	}
	new[n] = '\0';
    }
    else strcpy(new, old);

    return(new);
}
/*---------------------------------------------------------------
 * from presim.c
 *---------------------------------------------------------------
 */

static void
ivf_gate_def ()
{
    int             delay_time;
    int             incount = 0, outcount = 0;    
    char           *tok_ptr;
    int             i;
    char            gate_name[200];

    /* acquire our gate name  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);
    
    /* We want the last GATE_NAME_SIZE characters to use for the name */
    str_end_copy(gate_name, tok_ptr, GATE_NAME_SIZE);  /* Name limit Added 11-6-91 STF */

    /* verify we have our open brace  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    if (strcmp (tok_ptr, IVF_OPEN_STR))
    {
	fprintf (stderr, "found %s when expecting %s in .ivf file\n",
		 tok_ptr, IVF_OPEN_STR);
	exit (1);
    }

    /* read the gate type  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    /* add the gate to the database  */
    curobj_module = newobject(gate_name, tok_ptr);

    /* read the delay time  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    delay_time = check_int_str (tok_ptr);
    if (delay_time != 0)
    {
	adddelay (delay_time);
    }

    /* read the delay flag  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);
    if (!strcmp (tok_ptr, STR_DELAY_TRANSPORT))
    {
	/* a transport delay  */
	curobj_module->dly_type = TRANSPORT_DELAY;
    }
    else
    {
	/* an inertial delay  */
	curobj_module->dly_type = INERTIAL_DELAY;
    }


    /* get the number on inputs  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    incount = check_int_str (tok_ptr);
    
    /* get all the inputs  */
    for (i = 0; i < incount; i++)
    {
	tok_ptr = get_next_token ();
	CHK_IVF_END (tok_ptr);

	/* add the input to the list of inputs for this node  */
	addin (tok_ptr, i, incount);
    }

    /* get the number on outputs  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    outcount = check_int_str (tok_ptr);

    /* get all the outputs  */
    for (i = 0; i < outcount; i++)
    {
	tok_ptr = get_next_token ();
	CHK_IVF_END (tok_ptr);

	/* add the output to the list of outputs for this node  */
	addout (tok_ptr, i, outcount);
    }

    /* now that we have the counts we can tie them to the icon positions */
    addpositions(curobj_module, incount, 0, outcount);    

    /* get the terminating brace  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    if (strcmp (tok_ptr, IVF_CLOSE_STR))
    {
	fprintf (stderr, "illegal token, %s, found expected %s\n",
		 tok_ptr, IVF_CLOSE_STR);
	exit (1);
    }

}
/*---------------------------------------------------------------
 * stringEq - used to check the sensitivity list
 *---------------------------------------------------------------*/
int stringEq(s1, s2)
    char *s1, *s2;
{
    if (!strcmp(s1, s2)) return(TRUE);
    else return(FALSE);
}

/*---------------------------------------------------------------
 * ivf_proc_pinpositions - used to record fixed pin positions:
 *---------------------------------------------------------------*/
ivf_proc_pin_positions()
{
    char *tok_ptr, *netName;
    int count, i, x, y;

    /* get the FPPP openning brace */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);
    
    /* Read in the number of pins with fixed positions: */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);
    count = atoi(tok_ptr);

    for (i = 0; i < count; i++)
    {
	/* Read in the net name: */
	netName = strdup(get_next_token());

	/* Read in the x and y coordinates: */
	tok_ptr = get_next_token ();
	CHK_IVF_END (tok_ptr);
	x = atoi(tok_ptr);
	
	tok_ptr = get_next_token ();
	CHK_IVF_END (tok_ptr);
	y = atoi(tok_ptr);

	/* Do something interesting with this info: */
	fix_pin_position(curobj_module, netName, x, y);
    }

    /* get the FPPP terminating brace */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);
}
/*---------------------------------------------------------------
 * ivf_proc_icon_size - used to record a predefined icon size
 *---------------------------------------------------------------*/
ivf_proc_icon_size()
{
    char *tok_ptr;
    int x, y;

    /* get the FPIS openning brace */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);
    
    /* Read in the x and y coordinates: */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);
    x = atoi(tok_ptr);

    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);
    y = atoi(tok_ptr);

    reset_default_icon_size(curobj_module, x, y);

    /* get the FPIS terminating brace */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);
}
/*---------------------------------------------------------------
 * from presim.c		(Modified 2/91 STF)
 *---------------------------------------------------------------
 */

static void
ivf_proc_def ()
{
    list           *sensitivityList = NULL;
    char           *tok_ptr;
    char            proc_name[200];
    int             in_count = 0, inout_count = 0, out_count = 0;
    int             x, y, i, tempCount, index = 0;
    nptr            ntemp;
    
    /* acquire our process name  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    /* We want the last GATE_NAME_SIZE characters to use for the name */
    str_end_copy(proc_name, tok_ptr, GATE_NAME_SIZE);  /* Name limit Added 11-6-91 STF */
/*    strcpy (proc_name, tok_ptr); */

    /* verify we have our open brace  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    if (strcmp (tok_ptr, IVF_OPEN_STR))
    {
	fprintf (stderr, "found %s when expecting %s in .ivf file\n",
		 tok_ptr, IVF_OPEN_STR);
	exit (1);
    }

    /* read the long process name  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    /* add the process to the database  */
    curobj_module = newobject (proc_name, tok_ptr);

    /* get the number on items on the sensitivity list  */
    /* THE SENSITIVITY LIST IS IGNORED FOR NOW  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    inout_count = check_int_str (tok_ptr);	/* # items on sensitivity list */

    /* flush all the items on the sensitivity list  */
    for (i = 0; i < inout_count; i++)
    {
	tok_ptr = get_next_token ();
	CHK_IVF_END (tok_ptr);

	/* add the signal to the inout list  */
	addinout (tok_ptr, i, inout_count);

	/* add to a list to pull from input/output lists */
	push(strdup(tok_ptr), &sensitivityList);
#if 0        
        /*  OLD only point nodes at object which are in the sensitivity list  */
        ntemp = (nptr)getnode (tok_ptr);
        push ((lcontents) curobj_module, (lptr *) & ntemp->in);
        curobj_module->oflags = PROCESS_GATE;
#endif
    }

    /*
     * get the number of external signals, and add to inout lists
     */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    tempCount = in_count = check_int_str (tok_ptr);  /* inputs not on sensitivity list */

    /* get the signals  */
    for (i = 0; i < tempCount; i++)
    {
	tok_ptr = get_next_token ();
	CHK_IVF_END (tok_ptr);

	/* OLD: add the signal to the inout list OLD */
	/* addinout (tok_ptr, i, in_count);       */

	/* Add the string to the input list: */
	if (member_p(tok_ptr, sensitivityList, stringEq) == FALSE) 
	    addin(tok_ptr, index++, in_count);
	else in_count--;
    }
    index = 0;

    /* get the number of output variables  */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    tempCount = out_count = check_int_str (tok_ptr);/* outputs not on sensitivity list */

    /* get all the variables  */
    for (i = 0; i < tempCount; i++)
    {
	tok_ptr = get_next_token ();
	CHK_IVF_END (tok_ptr);

	/* Add the string to the output list: */
	if (member_p(tok_ptr, sensitivityList, stringEq) == FALSE) 
	    addout(tok_ptr, index++, out_count);
	else out_count--;
    }


    /* Now look for the optional icon size info: 	added 3-92 (stf) */
    tok_ptr = get_next_token ();
    CHK_IVF_END (tok_ptr);

    if (!strcmp(tok_ptr, FLAT_PROC_ICON_SIZE))
    {
	ivf_proc_icon_size();
	addpositions(curobj_module, in_count, inout_count, out_count);    
    
	/* get the terminating brace?? */
	tok_ptr = get_next_token ();
	CHK_IVF_END (tok_ptr);

	if (!strcmp(tok_ptr, FLAT_PROC_PIN_POSITIONS))
	{
	    ivf_proc_pin_positions();

	    /* Now get the terminating brace: */
	    tok_ptr = get_next_token ();
	    CHK_IVF_END (tok_ptr);
	}
    }
    else if (!strcmp(tok_ptr, FLAT_PROC_PIN_POSITIONS))
    {
	ivf_proc_pin_positions();
	
	/* Now get the terminating brace?? */
	tok_ptr = get_next_token ();
	CHK_IVF_END (tok_ptr);

	if (!strcmp(tok_ptr, FLAT_PROC_ICON_SIZE))
	{
	    ivf_proc_icon_size();
	    /* BUG NOTE: This won't work correctly:  "addpositions" will overwrite 
	       the work done in "ivf_proc_pin_positions" */
	    addpositions(curobj_module, in_count, inout_count, out_count); 
   
	    /* Now get the terminating brace: */
	    tok_ptr = get_next_token ();
	    CHK_IVF_END (tok_ptr);
	}
    }    
    else
    {
	/* now that we have the counts we can tie them to the icon positions */
	addpositions(curobj_module, in_count, inout_count, out_count);    	
    }

    if (strcmp (tok_ptr, IVF_CLOSE_STR))
    {
	fprintf (stderr, "illegal token, %s, found expected %s\n",
		 tok_ptr, IVF_CLOSE_STR);
	exit (1);
    }
    free_list(sensitivityList);
}
/*---------------------------------------------------------------
 * from presim.c
 *---------------------------------------------------------------
 */

check_int_str (str)
    char           *str;
{
    char           *s2;

    /* verify the specified string is a valid integer string  */

    for (s2 = str; *s2 != '\0'; s2++)
    {
	if (!isdigit (*s2))
	{
	    fprintf (stderr, "illegal character, %c, found in digit string\n", *s2);
	    return (-1);
	}
    }

    return (atoi (str));
}


/***********************************************************************************
 Add2TermModule - This method is used to add a new module. This can be used in HSPICE
             parser to add a module. 
             

**************************************************************************************/

void Add2TermModule( name, type, inNode, outNode )
char* name;		// Parser-supplied module name (e.g., CAP32)
char* type;		// Parser-supplied identification type (e.g., CAPACITOR)
char* inNode;		// Net name for input net
char* outNode;		// Net name for output net
{
   net* pNet;

   //Create a new Module( Capacitor or Resistor or Inductor or Buffer, Inverter gate etc)
   curobj_module = newobject(name, type);  

   //Add Inputports
   pNet = get_net(inNode);
   
   //If Input Node does not exist in the global database
   if( pNet == NULL )
   {
      newnode(inNode);
   }
   addin(inNode, 0, 1);

   //Add output ports
   pNet = get_net(outNode);
   
   //If output Node does not exist in the global database
   if( pNet == NULL )
   {
      newnode(outNode);
   }
   addout(outNode, 0, 1);
}

/***********************************************************************************
 Add3TermModule - This method is used to add a new module. This can be used in HSPICE
             parser to add a module. 
             

**************************************************************************************/

void Add3TermModule( name, type, inNode, outNode, inoutNode)
char* name;		// Parser-supplied module name (e.g., CAP32)
char* type;		// Parser-supplied identification type (e.g., CAPACITOR)
char* inNode;		// Net name for input (left) net
char* outNode;		// Net name for output (right) net
char* inoutNode;	// Net name for inout (top) net
{
   net* pNet;

   //Create a new Module( Capacitor or Resistor or Inductor or Buffer, Inverter gate etc)
   curobj_module = newobject(name, type);  

   //Add Inputports
   pNet = get_net(inNode);
   
   //If Input Node does not exist in the global database
   if( pNet == NULL )
   {
      newnode(inNode);
   }
   addin(inNode, 0, 1);

   //Add output ports
   pNet = get_net(outNode);
   
   //If output Node does not exist in the global database
   if( pNet == NULL )
   {
      newnode(outNode);
   }
   addout(outNode, 0, 1);

   //Add inout ports
   pNet = get_net(inoutNode);
   
   //If inout Node does not exist in the global database
   if( pNet == NULL )
   {
      newnode(inoutNode);
   }
   addinout(inoutNode, 0, 1);
}

/*----------------------------------------------------------------------*/
/* AddNTermModule ---							*/
/*	Add a module of N terminals to the database			*/
/*									*/
/* name	= Parser-supplied module name (e.g., CAP32)			*/
/* type	= Parser-supplied identification type (e.g., CAPACITOR)		*/
/* N    = Number of nodes, followed by list of node names.		*/
/* followed by pairs of char * types declaring the name of the pin	*/
/* (expected in the xcircuit object) followed by the name of the net.	*/
/*----------------------------------------------------------------------*/

void AddNTermModule(char *name, char *type, int N, ...)
{
   va_list args;
   int i;
   net *pNet;
   char *pinName;
   char *netName;

   //Create a new Module( Capacitor or Resistor or Inductor or Buffer, Inverter gate etc)
   curobj_module = newobject(name, type);  

   va_start(args, N);

   for (i = 0; i < N; i++) {
      // Add port
      pinName = va_arg(args, char *);
      netName = va_arg(args, char *);
      pNet = get_net(netName);
   
      // If Input Node does not exist in the global database
      if (pNet == NULL) {
	 newnode(netName);
      }
      add_xc_term(type, pinName, netName, i);
   }
   va_end(args);
}

/*---------------------------------------------------------------
 * END OF FILE
 *---------------------------------------------------------------
 */
