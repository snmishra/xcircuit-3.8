#ifndef _CALLING_H
#define _CALLING_H

#ifdef DLLEXPORT
  #define DECLSPEC __declspec(dllexport)
#else
  #define DECLSPEC __declspec(dllimport)
#endif

/* Define calling convention in one place, for convenience. */
#define CALLCONV __stdcall

#endif
