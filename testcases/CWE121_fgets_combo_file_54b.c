
//#include <inttypes.h> // for PRId64
#include <stdio.h>
#include <stdlib.h>
//#include <wctype.h>
#include "std_testcase.h"
#include <time.h>
#ifndef _WIN32
//#include <wchar.h>
#endif

int isxdigit(int c){
    return (c >= '0' && c <= '9') || (c >= 'A' && c <= 'F') || (c >= 'a' && c <= 'f');
}
int iswxdigit(wint_t wc){
    return isxdigit(wc);
}
void printLine (const char * line)
{
    if(line != NULL) 
    {
        printf("%s\n", line);
    }
}

void printWLine (const wchar_t * line)
{
    if(line != NULL) 
    {
        //wprintf(L"%ls\n", line);
    }
}

void printIntLine (int intNumber)
{
    printf("%d\n", intNumber);
}

void printShortLine (short shortNumber)
{
    printf("%hd\n", shortNumber);
}

void printFloatLine (float floatNumber)
{
    printf("%f\n", floatNumber);
}

void printLongLine (long longNumber)
{
    printf("%ld\n", longNumber);
}

void printLongLongLine (int64_t longLongIntNumber)
{
    printf("%" PRId64 "\n", longLongIntNumber);
}

void printSizeTLine (size_t sizeTNumber)
{
    printf("%zu\n", sizeTNumber);
}

void printHexCharLine (char charHex)
{
    printf("%02x\n", charHex);
}

void printWcharLine(wchar_t wideChar) 
{
    /* ISO standard dictates wchar_t can be ref'd only with %ls, so we must make a
     * string to print a wchar */
    wchar_t s[2];
        s[0] = wideChar;
        //s[1] = L'\0';
    printf("%ls\n", s);
}

void printUnsignedLine(unsigned unsignedNumber) 
{
    printf("%u\n", unsignedNumber);
}

void printHexUnsignedCharLine(unsigned char unsignedCharacter) 
{
    printf("%02x\n", unsignedCharacter);
}

void printDoubleLine(double doubleNumber) 
{
    printf("%g\n", doubleNumber);
}

void printStructLine (const twoIntsStruct * structTwoIntsStruct)
{
    printf("%d -- %d\n", structTwoIntsStruct->intOne, structTwoIntsStruct->intTwo);
}

void printBytesLine(const unsigned char * bytes, size_t numBytes)
{
    size_t i;
    for (i = 0; i < numBytes; ++i)
    {
        printf("%02x", bytes[i]);
    }
    puts("");	/* output newline */
}

/* Decode a string of hex characters into the bytes they represent.  The second
 * parameter specifies the length of the output buffer.  The number of bytes
 * actually written to the output buffer is returned. */
size_t decodeHexChars(unsigned char * bytes, size_t numBytes, const char * hex)
{
    size_t numWritten = 0;

    /* We can't sscanf directly into the byte array since %02x expects a pointer to int,
     * not a pointer to unsigned char.  Also, since we expect an unbroken string of hex
     * characters, we check for that before calling sscanf; otherwise we would get a
     * framing error if there's whitespace in the input string. */
    while (numWritten < numBytes && isxdigit(hex[2 * numWritten]) && isxdigit(hex[2 * numWritten + 1]))
    {
        int byte;
        sscanf(&hex[2 * numWritten], "%02x", &byte);
        bytes[numWritten] = (unsigned char) byte;
        ++numWritten;
    }

    return numWritten;
}

/* Decode a string of hex characters into the bytes they represent.  The second
 * parameter specifies the length of the output buffer.  The number of bytes
 * actually written to the output buffer is returned. */
 size_t decodeHexWChars(unsigned char * bytes, size_t numBytes, const wchar_t * hex)
 {
    size_t numWritten = 0;

    /* We can't swscanf directly into the byte array since %02x expects a pointer to int,
     * not a pointer to unsigned char.  Also, since we expect an unbroken string of hex
     * characters, we check for that before calling swscanf; otherwise we would get a
     * framing error if there's whitespace in the input string. */
    while (numWritten < numBytes && iswxdigit(hex[2 * numWritten]) && iswxdigit(hex[2 * numWritten + 1]))
    {
        int byte;
        //swscanf(&hex[2 * numWritten], L"%02x", &byte);
        bytes[numWritten] = (unsigned char) byte;
        ++numWritten;
    }

    return numWritten;
}

/* The two functions always return 1 or 0, so a tool should be able to 
   identify that uses of these functions will always return these values */
int globalReturnsTrue() 
{
    return 1;
}

int globalReturnsFalse() 
{
    return 0;
}

int globalReturnsTrueOrFalse() 
{
    return (rand() % 2);
}

/* The variables below are declared "const", so a tool should
   be able to identify that reads of these will always return their 
   initialized values. */
const int GLOBAL_CONST_TRUE = 1; /* true */
const int GLOBAL_CONST_FALSE = 0; /* false */
const int GLOBAL_CONST_FIVE = 5; 

/* The variables below are not defined as "const", but are never
   assigned any other value, so a tool should be able to identify that
   reads of these will always return their initialized values. */
int globalTrue = 1; /* true */
int globalFalse = 0; /* false */
int globalFive = 5; 

/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_54b.c
Label Definition File: CWE121_Stack_Based_Buffer_Overflow__CWE129.label.xml
Template File: sources-sinks-54b.tmpl.c
*/
/*
 * @description
 * CWE: 121 Stack Based Buffer Overflow
 * BadSource: fgets Read data from the console using fgets()
 * GoodSource: Larger than zero but less than 10
 * Sinks:
 *    GoodSink: Ensure the array index is valid
 *    BadSink : Improperly check the array index by not checking the upper bound
 * Flow Variant: 54 Data flow: data passed as an argument from one function through three others to a fifth; all five functions are in different source files
 *
 * */

#include "std_testcase.h"

#define CHAR_ARRAY_SIZE (3 * sizeof(data) + 2)

#ifndef OMITBAD

/* bad function declaration */
void CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_54c_badSink(int data);

void CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_54b_badSink(int data)
{
    CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_54c_badSink(data);
}

#endif /* OMITBAD */

#ifndef OMITGOOD

/* goodG2B uses the GoodSource with the BadSink */
void CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_54c_goodG2BSink(int data);

void CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_54b_goodG2BSink(int data)
{
    CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_54c_goodG2BSink(data);
}

/* goodB2G uses the BadSource with the GoodSink */
void CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_54c_goodB2GSink(int data);

void CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_54b_goodB2GSink(int data)
{
    CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_54c_goodB2GSink(data);
}

#endif /* OMITGOOD */