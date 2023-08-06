from .kernel import GnuplotKernel

try:
    from ipykernel.kernelapp import IPKernelApp
except ImportError:
    from IPython.kernel.zmq.kernelapp import IPKernelApp


IPKernelApp.launch_instance(kernel_class=GnuplotKernel)
