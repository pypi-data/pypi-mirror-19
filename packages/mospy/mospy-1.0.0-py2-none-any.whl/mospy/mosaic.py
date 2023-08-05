from Tkinter import *
from PIL import Image, ImageTk
from numpy import *
import os
import pickle
import show_images
from multiprocessing import Process, Queue, Pool

DATASETDIR = './pictures'
DATADIR = './rgbdata'
FILEDIR = './'
OUTFILENAME = 'mosaic.jpg'

NUM_PROCESS = 4
NUM_GRID = 8

def process_tile(file):
	tile = Image.open(os.path.join(DATASETDIR, file))
	tile_data = array(tile.getdata())
	avg_red = sum(tile_data[:, 0])/tile_data.shape[0]
	avg_green = sum(tile_data[:, 1])/tile_data.shape[0]
	avg_blue = sum(tile_data[:, 2])/tile_data.shape[0]

	data = (file, avg_red, avg_green, avg_blue)
	return data

def save_data():
	print('Saving Average Color Data')
	if not os.path.isdir(DATADIR):
		os.mkdir(DATADIR)

	files = os.listdir(DATASETDIR)
	processes = Pool(NUM_PROCESS)
	result = processes.map(process_tile, files, NUM_PROCESS)
	total = len(result)
	result.append((DATASETDIR, total, total, total))

	with open(os.path.join(DATADIR, 'avg.dat'), 'w') as f:
		pickle.dump(result, f)



def load_data():
	avg_data = []
	if os.path.isfile(os.path.join(DATADIR, 'avg.dat')):
		avg_data = pickle.load(open(os.path.join(DATADIR, 'avg.dat'), 'r'))
		return avg_data

	return avg_data

def get_nearest_tile(grid, all_avgs):
	grid_data = array(grid.getdata())

	avg_red = sum(grid_data[:, 0])/grid_data.shape[0]
	avg_green = sum(grid_data[:, 1])/grid_data.shape[0]
	avg_blue = sum(grid_data[:, 2])/grid_data.shape[0]
	min_diff = sys.maxint

	best_tile = None
	for avg in all_avgs:
		diff = sqrt(square(avg[1]-avg_red)+square(avg[2]-avg_green)+square(avg[3]-avg_blue))
		if diff < min_diff:
			min_diff = diff
			best_tile = avg[0]

	return best_tile

def place_tiles(args):
	i = args[0]
	num_grids = args[1]
	avgs = args[2]
	mos_img = args[3]
	width = mos_img.size[0]
	height = mos_img.size[1]

	x_size = width/num_grids
	y_size = height/num_grids

	for j in range(num_grids):
		cords = (min(j*x_size, width), min(i*y_size, height))
		next_cords = (min((j+1)*x_size, width), min((i+1)*y_size, height))

		grid = mos_img.crop((cords[0], cords[1], next_cords[0], next_cords[1]))
		best_tile = get_nearest_tile(grid, avgs)
		tile = Image.open(os.path.join(DATASETDIR, best_tile))
		tile = tile.resize(grid.size)
		tile_data = tile.getdata()
		temp_img = Image.new('RGB', grid.size)
		temp_img.putdata(tile_data)

		mos_img.paste(temp_img, (cords[0], cords[1], next_cords[0], next_cords[1]))

	return [i, mos_img]

def build_mosaic(filename, num_grids=NUM_GRID, root=None, datasetdir=DATASETDIR):
	global DATASETDIR
	DATASETDIR = datasetdir
	mos_img = Image.open(filename)
	width = mos_img.size[0]
	height = mos_img.size[1]

	x_size = width/num_grids
	y_size = height/num_grids
	avgs = load_data()

	if len(avgs)==0 or avgs[-1][0] != datasetdir:
		save_data()
		avgs = load_data()

	avgs = avgs[:-1]

	workers = Pool(4)
	data = []
	for i in range(num_grids):
		data.append([i, num_grids, avgs, mos_img])

	result = workers.map(place_tiles, data, 4)

	final_image = Image.new('RGB', mos_img.size)

	for image_data in result:
		i = image_data[0]
		image = image_data[1]
		cords = (0, min(i*y_size, height))
		next_cords = (width, min((i+1)*y_size, height))
		box = (cords[0], cords[1], next_cords[0], next_cords[1])
		row = image.crop(box)
		final_image.paste(row, box)


	final_image.save(os.path.join(FILEDIR, OUTFILENAME))
	show_images.show_images(OUTFILENAME, root)