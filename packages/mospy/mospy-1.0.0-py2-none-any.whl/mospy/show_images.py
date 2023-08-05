from Tkinter import *
from PIL import Image, ImageTk
import os

FILEDIR = './'

class VerticalScrolledFrame(Frame):
    def __init__(self, parent, *args, **kw):
		Frame.__init__(self, parent, *args, **kw)            

		# create a canvas object and a vertical scrollbar for scrolling it
		vscrollbar = Scrollbar(self, orient=VERTICAL)
		vscrollbar.pack(fill=Y, side=RIGHT, expand=False)

		hscrollbar = Scrollbar(self, orient=HORIZONTAL)
		hscrollbar.pack(fill=X, side=BOTTOM, expand=False)


		canvas = Canvas(self, bd=0, highlightthickness=0,
		                yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
		canvas.pack(side=LEFT, fill=BOTH, expand=True)
		vscrollbar.config(command=canvas.yview)
		hscrollbar.config(command=canvas.xview)

		# reset the view
		canvas.xview_moveto(0)
		canvas.yview_moveto(0)

		# create a frame inside the canvas which will be scrolled with it
		self.interior = interior = Frame(canvas)
		interior_id = canvas.create_window(0, 0, window=interior,
		                                   anchor=NW)

		# track changes to the canvas and frame width and sync them,
		# also updating the scrollbar
		def _configure_interior(event):
		    # update the scrollbars to match the size of the inner frame
		    size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
		    canvas.config(scrollregion="0 0 %s %s" % size)
		    if interior.winfo_reqwidth() != canvas.winfo_width():
		        # update the canvas's width to fit the inner frame
		        canvas.config(width=interior.winfo_reqwidth())
		interior.bind('<Configure>', _configure_interior)

		def _configure_canvas(event):
		    if interior.winfo_reqwidth() != canvas.winfo_width():
		        # update the inner frame's width to fill the canvas
		        canvas.itemconfigure(interior_id, width=canvas.winfo_width())
		canvas.bind('<Configure>', _configure_canvas)


def show_images(im, root=None):
	img = Image.open(os.path.join(FILEDIR, im))
	if root == None:
		root = Tk()
	
	root.title("Mosaic Image")
	root.geometry('%dx%d+%d+%d' % (img.size[0]+50, img.size[1]+50 , 100, 100))
	
	if hasattr(root, 'imageframe'):
		root.imageframe.destroy()

	root.imageframe = VerticalScrolledFrame(root)

	root.imageframe.pack(fill=BOTH, expand=True)
	
	imgtk = ImageTk.PhotoImage(img)

	panel = Label(root.imageframe.interior, image=imgtk)
	
	panel.pack()


	root.mainloop()