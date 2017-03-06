#!/bin/bash
#SBATCH -p short
#SBATCH -n 1
#SBATCH --time=00:30:00 --mem-per-cpu=6000
#SBATCH --array=75-77

GEOMETRY_FILE="tip-sample_axisymmetry.geo"
PROBLEM_DEF_FILE="tip-sample_axisymmetry.pro"
RESOLUTION="EleSta_v"
POST_PROCESSING="Map_interp"
V_MESH_FILE="tip-sample_v.pos"
V_GRID_FILE="v_cut_grid.txt"

RUN_DIR=$PWD
JOB_DIR=$RUN_DIR/job_$SLURM_ARRAY_TASK_ID

cd $TMPDIR
cp $JOB_DIR/* .
cp $RUN_DIR/EleSta_v.pro .
cp $RUN_DIR/Integration_Lib.pro .
cp $RUN_DIR/Jacobian_Lib.pro .

gmsh $GEOMETRY_FILE -2
getdp $PROBLEM_DEF_FILE -solve $RESOLUTION -pos $POST_PROCESSING

python fem_mesh_to_grid_interpolation.py $V_MESH_FILE $V_GRID_FILE 

rm *.geo
rm *.pro
rm *.msh
rm *.pre
rm *.res
rm *.pos

mv $TMPDIR/* $JOB_DIR/
