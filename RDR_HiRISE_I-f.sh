echo $1
rm -f RDRCUMINDEX.TAB
wget https://hirise-pds.lpl.arizona.edu/PDS/INDEX/RDRCUMINDEX.TAB

mkdir $1

cd $1

link=`cat ../RDRCUMINDEX.TAB | grep $1 | grep COLOR | awk '{print "https://hirise-pds.lpl.arizona.edu/PDS/"substr($0,15,67)}'`
wget $link

lbllink=`echo $link | sed s/"JP2"/"LBL"/`
wget $lbllink

sf=`cat ${1}_COLOR.LBL | grep SCALING_FACTOR | tail -1 | awk '{printf "%.20f", $3}'`
offset=`cat ${1}_COLOR.LBL | grep OFFSET | tail -1 | awk '{printf "%.14f", $3}'`
incidence_angle=`cat ${1}_COLOR.LBL | grep NCIDENCE_ANGLE | tail -1 | awk '{printf "%.8f", $3}'`
pi=`echo "4*a(1)" | bc -l`
rad_angle=`echo "${incidence_angle}*(${pi}/180)" | bc -l`
cosine_incidence_angle=`echo "c(${rad_angle})" | bc -l`

echo $sf
echo $offset
echo $incidence_angle
echo $cosine_incidence_angle

echo "Calculating I/F for: "$1" ..."
gdal_calc.py --A_band=1 --type=Float32 -A ${1}_COLOR.JP2 --format=HFA --outfile=${1}_COLOR_IF_R.img --calc="(A*${sf}+${offset})/${cosine_incidence_angle}"
echo "Doing no. 2"
gdal_calc.py --A_band=2 --type=Float32 -A ${1}_COLOR.JP2 --format=HFA --outfile=${1}_COLOR_IF_G.img --calc="(A*${sf}+${offset})/${cosine_incidence_angle}"
echo "Doing no. 3"
gdal_calc.py --A_band=3 --type=Float32 -A ${1}_COLOR.JP2 --format=HFA --outfile=${1}_COLOR_IF_B.img --calc="(A*${sf}+${offset})/${cosine_incidence_angle}"

echo "Merging..."
gdal_merge.py -o ${1}_COLOR_IF.img -of HFA -separate ${1}_COLOR_IF_R.img ${1}_COLOR_IF_G.img ${1}_COLOR_IF_B.img 

echo "Finished Calculating I/F for: "$1

rm -f *.JP2
rm -f *.LBL

cd ..
