#!/bin/sh
#
# This script starts xcircuit under the Tcl interpreter,
# reading commands from a special .wishrc script which
# launches magic and retains the Tcl interactive interpreter.
#

loclibdir=${XCIRCUIT_LIB_DIR:=/usr/local/lib/xcircuit-3.8}
export XCIRCUIT_LIB_DIR
XCIRCUIT_WISH=/usr/local/bin/wish8.5
export XCIRCUIT_WISH

# Hacks for Cygwin
if [ ${TERM:=""} = "cygwin" ]; then
   export PATH=$PATH:/usr/local/lib
   export DISPLAY=${DISPLAY:=":0"}
fi

TKCON=true
for i in $@ ; do
   case $i in
      -noc*)
	   TKCON=;;
      --help)
	   echo "Standard usage:"
	   echo "   xcircuit [filename]"
	   echo "Online documentation:"
	   echo "   http://opencircuitdesign.com/xcircuit"
	   exit 0
	   ;;
      --version)
	   echo "XCircuit version 3.8 revision 8"
	   exit 0
	   ;;
   esac
done

if [ $TKCON ]; then

   if [ ! -f ${loclibdir}/tkcon.tcl ]; then
      loclibdir=${loclibdir}/tcl
   fi

   exec ${loclibdir}/tkcon.tcl \
	-eval "source ${loclibdir}/console.tcl" \
        -slave "package require Tk; set argc $#; set argv [list $*]; \
        source ${loclibdir}/xcircuit.tcl"
else

#
# Run the stand-in for wish (xcircexec), which acts exactly like "wish"
# except that it replaces ~/.wishrc with xcircuit.tcl.  This executable is
# *only* needed when running without the console; the console itself is
# capable of sourcing the startup script.
#
   exec ${loclibdir}/xcircexec -- $@

fi
