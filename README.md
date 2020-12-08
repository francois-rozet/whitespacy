# Whitespacy

Whitespacy is a [polyglot](https://en.wikipedia.org/wiki/Polyglot_(computing)) formatter, written in [Python](https://en.wikipedia.org/wiki/Python_(programming_language)), for the [C](https://en.wikipedia.org/wiki/C_(programming_language)) and [Whitespace](https://en.wikipedia.org/wiki/Whitespace_(programming_language)) programming languages.

It takes as input a valid C file and a valid Whitespace file, and produces, as output, a polyglot file that is valid in both C and Whitespace, while behaving *exaclty* like the inputs when interpreted/compiled.

> Whitespacy also includes [`minic.py`](minic.py), a simple C-minifier.

## But why ?

The goal of the project was to demonstrate that it is possible to embbed a fully functionnal Whitespace program withing the whitespace characters (` `, `\t` and `\n`) of a program written in another language.

Is it useless ? For sure. Is it trivial ? Hell no.

## Dependencies

Whitespacy only uses the standard libraries of Python. However, if you wish to compile the C files, you will need a C compiler like `gcc` or `clang`.

To interpret the Whitespace files, I have used an [online Whitespace interpreter](https://naokikp.github.io/wsi/whitespace.html).

## Example

Let's take as inputs this (nice) "Hello, World!" C program

```C
#include <stdio.h>

#define NICE 69420

int isNice(int x) {
    return x == NICE;
}

/* tricky quote " */
#define min(x, y) \
((x) < (y) ? (x) : (y))

int main() {
    printf("Hello, World!\n");

    if (isNice(3 * 4 * 5 * min(13, 31) * 89))
        printf("nice.\n");

    /* tricky //
       string */
    if (0)
        printf("/* */ \" // \
        ");

    return 0; // no error
}
```

and a basic "Hello, World!" Whitespace program (see [`hello-world.ws`](hello-world.ws)).

Then, running the command

```bash
python whitespacy.py hello-world.c hello-world.ws -o polyglot.c
```

produces the [`polyglot.c`](polyglot.c) file

```C
#   	  	   include<stdio.h>
	
   #define NICE 		  	 	69420
	
int  isNice   	(	 		int x){return x==NICE;}
	
#     		define min(x		 ,y)((x)<(y)?(x):(y) )
	
     		 				
	
     	 		  
	
     	     
	
     			 			
	
    int main(){printf("Hello,\x20World!\n");if(isNice	(3*4*5*min(13,31)*89)	 				
	
    )printf("nice.\n");if(0 			  	 )printf("/*\x20*/\x20\"\x20//\x20\x20\x20\x20\x20\x20\x20\x20\x20");
	
 return    		 0;		  
	
     		  	  
	
     	    	
	
  


}
```

which, can be compiled with `gcc` (`clang`)

```bash
gcc polyglot.c -o polyglot
./polyglot
Hello, World!
nice.
```

or interpreted in Whitespace:

```txt
Hello, world!
```

> It should be noted that the output of [`whitespacy.py`](whitespacy.py) is different for each execution, as (part of) the formatting is randomly generated.
