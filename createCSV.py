import math, argparse, re, os, datetime, sys
from subprocess import Popen, PIPE
import pandas

def main():
  parser = argparse.ArgumentParser(prog='createJson', usage='%(prog)s [options]')
  parser.add_argument('txtFiles', metavar='files', nargs='+', help = 'The path to the text file')
  args = parser.parse_args()
  
  data_dict = {"analysis":[], "chromosome":[], "log_pvalue":[], "position":[], "pvalue":[], "ref_allele":[], "variant":[], "ref_allele_freq":[]}
  for txtf in args.txtFiles:
    analysis = os.path.basename(txtf).split('.')[0].strip()
    print analysis
    with open(txtf, 'r') as infile:
      for line in infile.readlines():
        if not line.startswith(b'#'):
          fields = line.split('\t')
          data_dict["analysis"].append(analysis)
          data_dict["chromosome"].append(fields[0].strip())
          data_dict["position"].append(int(fields[1].strip()))
          data_dict["variant"].append(fields[2].strip())
          ref_allele = fields[2].strip().split('_')[1].split('/')[0]
          data_dict["ref_allele"].append(ref_allele)
          data_dict["ref_allele_freq"].append(round(float(fields[4].strip()), 4))
          pvalue = float(fields[3].strip())
          logp = -math.log(pvalue, 10)
          data_dict["pvalue"].append(pvalue)
          data_dict["log_pvalue"].append(logp)

  df = pandas.DataFrame(data_dict)
  df.to_csv('assoc.csv', sep=',', index=False)
        
if __name__ == "__main__":
  main()
