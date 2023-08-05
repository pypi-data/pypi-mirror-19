import sys
import os
import mosaic

def main():
	args = sys.argv
	try:
		numgrids = int(args[1])
		dataset = os.path.abspath(args[2])
		target = os.path.abspath(args[3])
	except Exception:
		print('Usage : pymos <number of grids> <directory path of image dataset> <image name for mosaic>')
		return

	mosaic.build_mosaic(target, num_grids=numgrids, datasetdir=dataset)


