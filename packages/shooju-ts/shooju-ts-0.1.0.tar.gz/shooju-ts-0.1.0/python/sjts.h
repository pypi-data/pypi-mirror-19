
typedef struct __SJContext
{
  const char *name;
  Py_ssize_t len;
  PyObject *obj;
} SJContext;

typedef struct __SJResponse
{
  char *buffer;
  size_t sz;
  size_t nextSz;
  Py_ssize_t len;
  JSUINT64 pntSz;
  PyObject *obj;
} SJResponse;

PyObject *ProcessResponses(char *rootBuffer, SJResponse *responses, Py_ssize_t nResp);
extern PyObject *SJException;

#define SJ_ERR(fmt) PyErr_Format(SJException, fmt)
#define SJ_ERR1(fmt, v1) PyErr_Format(SJException, fmt, v1)
#define SJ_RESPONSES_KEY ("series")
