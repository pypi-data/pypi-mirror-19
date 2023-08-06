#include <Python.h>

unsigned long long int hex_to_int(PyObject *list, int size) {

  unsigned long long int t = 0LL;
  unsigned long long int temp;
  long val;
  int b;
  int i;

  PyObject *intObj;      /* one int in the list */

  for(i = 0; i < size; i++) {

    intObj = PyList_GetItem(list, i);
    val = PyInt_AsLong( intObj );

    temp = 0LL;
    b = size - (i + 1);
    temp += val;
    t += temp << (b << 3);
  }

  return t; 
} 

static PyObject* py_hex_to_int(PyObject* self, PyObject* args)
{

  // char * tok;          delimiter tokens for strtok 
  // int cols;            number of cols to parse, from the left 

  int n_elems;             /* how many lines we passed for parsing */
  // char * token;        token parsed by strtok 

  PyObject *listObj;     /* the list of elems */

  /* the O! parses for a Python object (listObj) checked
     to be of type PyList_Type */
  if (! PyArg_ParseTuple( args, "O!", &PyList_Type, &listObj)) return NULL;

  /* get the number of lines passed to us */
  n_elems = PyList_Size(listObj);

  /* should raise an error here. */
  if (n_elems < 0)   return NULL; /* Not a list */

  return Py_BuildValue("i", hex_to_int(listObj, n_elems));
}



int command_CRC(char *BitString)
   {
   //static char Res[9];                                 // CRC Result
   int Res = 0;
   char CRC[8];
   int  i;
   char DoInvert;
   
   for (i=0; i<8; ++i)  CRC[i] = 0;                    // Init before calculation
   
   for (i=0; i<strlen(BitString); ++i)
      {
      DoInvert = ('1'==BitString[i]) ^ CRC[7];         // XOR required?

      CRC[7] = CRC[6] ^ DoInvert;
      CRC[6] = CRC[5];
      CRC[5] = CRC[4];
      CRC[4] = CRC[3];
      CRC[3] = CRC[2];
      CRC[2] = CRC[1] ^ DoInvert;
      CRC[1] = CRC[0];
      CRC[0] = DoInvert;
      }
      
   for (i=0; i<8; ++i)  Res += CRC[i] << (i);
   return(Res);
}

static PyObject* py_command_CRC(PyObject* self, PyObject* args)
{
  char *b;
  PyArg_ParseTuple(args, "s", &b);
  return Py_BuildValue("i", command_CRC(b));
}


int response_CRC(char *BitString)
   {
   //static char Res[9];                                 // CRC Result
   //char BitString_mut[] = BitString; 
   int Res = 0;
   char CRC[7];
   int  i;
   char DoInvert;
   
   for (i=0; i<7; ++i)  CRC[i] = 0;                    // Init before calculation
   
   // Snooper always returns sync field as "11"
   // ICD reports sync field should always be "01"
   // CRC check works if replacing this
   // Faster to hack in fix here, than in python 
   // *BitString = "0";
   // # !! TO DO THIS, WE INIT THE LOOP FROM 1, NOT 0
   // # !! AS 0b0111 = 0b111 
   for (i=1; i<strlen(BitString); ++i)
      {
      DoInvert = ('1'==BitString[i]) ^ CRC[6];         // XOR required?

      CRC[6] = CRC[5];
      CRC[5] = CRC[4] ^ DoInvert;
      CRC[4] = CRC[3];
      CRC[3] = CRC[2] ^ DoInvert;
      CRC[2] = CRC[1];
      CRC[1] = CRC[0];
      CRC[0] = DoInvert;
      }
      
   for (i=0; i<7; ++i)  Res += CRC[i] << (i);

   return(Res);
}

static PyObject* py_response_CRC(PyObject* self, PyObject* args)
{
  char *b;
  PyArg_ParseTuple(args, "s", &b);
  return Py_BuildValue("i", response_CRC(b));
}


/*
 * Bind Python function names to our C functions
 */
static PyMethodDef utils_method[] = {
  {"command_CRC", py_command_CRC, METH_VARARGS},
  {"response_CRC", py_response_CRC, METH_VARARGS},
  {"hex_to_int", py_hex_to_int, METH_VARARGS},
  {NULL, NULL}
};

/*
 * Python calls this to let us initialize our module
 */
void initutils()
{
  (void) Py_InitModule("utils", utils_method);
}