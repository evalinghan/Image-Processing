cd Data/Extract_mb_79/

for i in *.tif; do

	root=`echo $i | sed s/\.tif//`
	echo $root

	gdal_translate -of GMT -b 1 $i ${root}_IR.grd
	gdal_translate -of GMT -b 2 $i ${root}_RED.grd
	gdal_translate -of GMT -b 3 $i ${root}_BG.grd

	echo extracting_IR

	grd2xyz ${root}_IR.grd | grep -v "\-3.40282346639e+38" > ${root}_IR.xyz

	total=`cat ${root}_IR.xyz | wc -l`
	n=1
	fid=`echo $i | sed s/"_"/" "/g | sed s/".tif"/""/ | awk '{print $7}'`
	while [ ${n} -le ${total} ]; do
		echo ${fid} >> a
		n=`echo ${n} + 1 | bc -l`
	done
	paste a ${root}_IR.xyz | awk '{print $1","$2","$3","$4}' > ${root}_FID_IR.xyz
	rm -f a

	echo extracting_RED

	grd2xyz ${root}_RED.grd | grep -v "\-3.40282346639e+38" > ${root}_RED.xyz

	total=`cat ${root}_RED.xyz | wc -l`
	n=1
	fid=`echo $i | sed s/"_"/" "/g | sed s/".tif"/""/ | awk '{print $7}'`
	while [ ${n} -le ${total} ]; do
		echo ${fid} >> a
		n=`echo ${n} + 1 | bc -l`
	done
	paste a ${root}_RED.xyz | awk '{print $1","$2","$3","$4}' > ${root}_FID_RED.xyz
	rm -f a

	echo extracting_BG

	grd2xyz ${root}_BG.grd | grep -v "\-3.40282346639e+38" > ${root}_BG.xyz

	total=`cat ${root}_BG.xyz | wc -l`
	n=1
	fid=`echo $i | sed s/"_"/" "/g | sed s/".tif"/""/ | awk '{print $7}'`
	while [ ${n} -le ${total} ]; do
		echo ${fid} >> a
		n=`echo ${n} + 1 | bc -l`
	done
	paste a ${root}_BG.xyz | awk '{print $1","$2","$3","$4}' > ${root}_FID_BG.xyz
	rm -f a

	cat ${root}_FID_IR.xyz | sed s/","/" "/g | awk '{print $1}' > a
	cat ${root}_FID_IR.xyz | sed s/","/" "/g | awk '{print $2}' > b
	cat ${root}_FID_IR.xyz | sed s/","/" "/g | awk '{print $3}' > c
	cat ${root}_FID_IR.xyz | sed s/","/" "/g | awk '{print $4}' > d
	cat ${root}_FID_RED.xyz | sed s/","/" "/g | awk '{print $4}' > e
	cat ${root}_FID_BG.xyz | sed s/","/" "/g | awk '{print $4}' > f

	paste a b c d e f | awk '{print $1","$2","$3","$4","$5","$6}' >> all-rasters.xyz
	rm -f a b c d e f *.xml ${root}_FID_IR.xyz ${root}_FID_RED.xyz ${root}_FID_BG.xyz *.grd ${root}_IR.xyz ${root}_RED.xyz ${root}_BG.xyz
	
done
