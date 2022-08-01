list1=$1 # Input file
type=$2 # Output folder name

script=/PATH/script # Your scripts

input_path=/PATH/${list1} # Input file (.bed): Chrom\tChromStart\tChromEnd\tComplementaryStrand
out_path=/PATH/${type} # Your ouput folder

if [ ! -d ${out_path}/tmp ]
then mkdir -p ${out_path}/tmp
fi

# Step 1: Prepare the input file
less ${input_path} | awk '{print $1,$4,$2}' | awk '{if($3*1>200) print $0}'  > ${out_path}/tmp/input_file.txt && \

# Step 2: Extract 3-mer sequences
bash run_step1.sh input_file ${type}

# Step 3: Generate the result file
cp run_step2.sh ${out_path}/tmp
cd ${out_path}/tmp
bash run_step2.sh && echo "${type} done"
