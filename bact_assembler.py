import os
import argparse


def fastq_files(file):    

    samples ={ i : os.listdir(file + i) for i in os.listdir(file) if "ds." in i  }
    
    return samples

def create_result_files(file, sample):
    if not os.path.isdir(file +  "results/" + sample):
        os.system(f"mkdir {file}results/{sample}")
    return f"{file}results/{sample}"


def quality_controls(fastq , res_file, s ):
    os.system(f"fastqc {fastq}/*.gz -o {res_file}")
    
    if not os.path.isdir(res_file +"/filtered_fastq"):
        os.system(f"mkdir {res_file}/filtered_fastq")

    os.system(f"fastp -i {fastq}/{os.listdir(fastq)[0]} -I {fastq}/{os.listdir(fastq)[1]} -o {res_file}/filtered_fastq/{s}_R1_fastq.fastq.gz -O {res_file}/filtered_fastq/{s}_R2_fastq.fastq.gz -g -f 15 -l 50 --adapter_fasta adapters.fa --failed_out {res_file}/failed --trim_tail1 5")
    os.system(f"fastqc {res_file}/filtered_fastq/*.gz -o {res_file}")
    
    if not os.path.isdir(res_file +"/assembly"):
        os.system(f"mkdir {res_file}/assembly")    
        
    os.system(f"spades -1 {res_file}/filtered_fastq/{s}_R1_fastq.fastq.gz -2 {res_file}/filtered_fastq/{s}_R2_fastq.fastq.gz -o {res_file}/assembly -t 48 ")    
    
    os.system(f"cp {res_file}/assembly/scaffolds.fasta  {args.input_path}results/all_assemblies/{s}_scaffolds.fasta")
    assert(0)


parser = argparse.ArgumentParser(description='An efficient way to process bacterial whole genome single and paired-end data',  epilog = "author: Maria Malliarou <maria.malliarou.ger@gmail.com> v1.1" )

parser.add_argument('--input_path',  type = str, required = True, help = "Please provide your fastq_folder" )  
parser.add_argument('--ref', type = str , help = 'Provide fill pathed reference')

args = parser.parse_args()


if args.input_path.endswith("/") == False:
    args.input_path = args.input_path + "/"

files = fastq_files(args.input_path)
print(os.listdir(args.input_path))
if not os.path.isdir(args.input_path+ "results"):
    os.system(f"mkdir {args.input_path}results")

os.system(f"mkdir {args.input_path}results/all_assemblies")
for f in files:
    #print(f)
    sample = f.split("_ds.")[0]
    res = create_result_files(args.input_path, sample)
    if os.path.isfile(f"{res}/assembly/scaffolds.fasta"):
        os.system(f"cp {res}/assembly/scaffolds.fasta  {args.input_path}results/all_assemblies/{sample}_scaffolds.fasta")
    else:
        quality_controls(args.input_path + f , res, sample)
 
    