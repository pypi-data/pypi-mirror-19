import subprocess,sprint,os,sys

def main(): 
    print ''
    print "##############################################################################################"
    print ''
    print "   SPRINT: SNP-free RNA editing Identification Toolkit"
    print ""
    print "   http://sprint.tianlab.cn/SPRINT/"
    print ""
    print "   Please contact with 15110700005@fudan.edu.cn when questions arise."
    print ""
    print "##############################################################################################"
    
    
    def help_doc():
        print ""
        print "   Attention:"
        print ""
        print "      Before using sprint_main, please use sprint_prepare to build mapping index."
        print ""
        print "   Usage:"
        print ""
        print "      sprint main   [options]   read(.fq)   reference_genome(.fa)   output_path   bwa_path   samtools_path"
        print ""
        print "      options:"
        print "         -rp repeat_file #Download from http://sprint.software/SPRINT/dbrep/"
        print "         -2  read2(.fq)  #Optional"
        print "         -c  INT         #Remove the fist INT bp in reads (default is 6)"
        print "         -p  INT         #Mapping CPU (default is 1)"
        print ""
        print "   Example:"
        print ""
        print "       sprint main -rp hg19_repeat.txt -c 6 -p 6 -2 read2.fq read1.fq hg19.fa output ./bwa-0.7.12/bwa ./samtools-1.2/samtools"
        print ""
        print ""
        print ""
        #print sys.argv[0]
        
        sys.exit(0)
    
    
    if len(sys.argv)<2:
        #print sys.argv[0]
        help_doc()
    
    
    
    cutbp=6
    cluster_distance=200
    mapcpu = 1
    
    
    paired_end=False
    repeat=False
    options=[]
    read2=''
    #print sys.argv
    i=1
    while i< len(sys.argv):
        if sys.argv[i]=='-2':
            paired_end=True
            try:
                read2=sys.argv[i+1]
                options.append(i)
                options.append(i+1)
            except Exception, e:
                print 'options error!'
                help_doc()
                exit()
        elif sys.argv[i]=='-rp':
            try:
                repeat=sys.argv[i+1]
                options.append(i)
                options.append(i+1)
            except Exception, e:
                print 'options error!'
                help_doc()
                exit()
        elif sys.argv[i]=='-c':
            try:
                cutbp=int(sys.argv[i+1])
                options.append(i)
                options.append(i+1)
            except Exception, e:
                print 'options error!'
                help_doc()
                exit()
        elif sys.argv[i]=='-p':
            try:
                mapcpu=int(sys.argv[i+1])
                options.append(i)
                options.append(i+1)
            except Exception, e:
                print 'options error!'
                help_doc()
                exit()
    
    
        i += 1
    
    all_argv=[]
    i=1
    while i< len(sys.argv):
        if i not in options:
            all_argv.append(i)
        i=i+1
    
    if len(all_argv)!=5:
        help_doc()
        exit()
    
    
    read1=sys.argv[all_argv[0]]
    refgenome=sys.argv[all_argv[1]]
    output=sys.argv[all_argv[2]]
    tmp=output+'/tmp/'
    #if output[-1]!='/':
    #    tmp=output+'.tmp/'
    #else:
    #    tmp=output[:-1]+'.tmp/'
    bwa=sys.argv[all_argv[3]]
    samtools=sys.argv[all_argv[4]]
    
    if os.path.exists(output)==False:
            os.mkdir(output)
    if os.path.exists(tmp)==False:
            os.mkdir(tmp)
    
    if paired_end==True:
        mapcpu=max([int(mapcpu)/2.0,1])
    
    
    
    
    
    def fq2sam(TAG,paired_end,read1,read2,tmp,refgenome,bwa,samtools):
        ori_tmp=tmp
        tmp=tmp+'/'+TAG+'/'
        if os.path.exists(tmp)==False:
            os.mkdir(tmp)
        step1_1=subprocess.Popen(bwa+' aln -t '+str(mapcpu)+' '+refgenome+' '+read1+' > '+tmp+'read1.sai',shell=True)
        if paired_end==True:
            step1_2=subprocess.Popen(bwa+' aln -t '+str(mapcpu)+' '+refgenome+' '+read2+' > '+tmp+'read2.sai',shell=True)
        step1_1.wait()
        if paired_end==True:
            step1_2.wait()
        step1_3=subprocess.Popen(bwa+' samse -n4 '+refgenome+' '+tmp+'read1.sai '+read1+' > '+tmp+'name_read1.sam',shell=True)
        if paired_end==True:
            step1_4=subprocess.Popen(bwa+' samse -n4 '+refgenome+' '+tmp+'read2.sai '+read2+' > '+tmp+'name_read2.sam',shell=True)
        step1_3.wait()
        if paired_end==True:
            step1_4.wait()
        if os.path.exists(tmp+'name_read1.sam'):
            if os.path.exists(tmp+'read1.sai'):
                    os.remove(tmp+'read1.sai')
            if os.path.exists(tmp+'cut_read1.fastq'):
                    os.remove(tmp+'cut_read1.fastq')
        if os.path.exists(tmp+'name_read2.sam'):
            if os.path.exists(tmp+'read2.sai'):
                    os.remove(tmp+'read2.sai')
            if os.path.exists(tmp+'cut_read2.fastq'):
                    os.remove(tmp+'cut_read2.fastq')
    
        #sprint.change_sam_read_name(tmp+'read1.sam',tmp+'name_read1.sam','read1')
        #if paired_end==True:
        #    sprint.change_sam_read_name(tmp+'read2.sam',tmp+'name_read2.sam','read2')
        step1_7=subprocess.Popen(samtools+' view -bS '+tmp+'name_read1.sam >'+tmp+'name_read1.bam',shell=True)
        if paired_end==True:
            step1_8=subprocess.Popen(samtools+' view -bS '+tmp+'name_read2.sam >'+tmp+'name_read2.bam',shell=True)
        step1_7.wait()
        if paired_end==True:
            step1_8.wait()
        if paired_end==True:
            step1_9=subprocess.Popen(samtools+' sort '+tmp+'name_read1.bam '+tmp+'name_read1_sorted',shell=True)
            step1_10=subprocess.Popen(samtools+' sort '+tmp+'name_read2.bam '+tmp+'name_read2_sorted',shell=True)
            step1_9.wait()
            step1_10.wait()
            step1_11=subprocess.Popen(samtools+' merge -f '+tmp+'all.bam '+tmp+'name_read1_sorted.bam '+tmp+'name_read2_sorted.bam',shell=True)
            step1_11.wait()
            if os.path.exists(tmp+'all.bam'):
                    if os.path.exists(tmp+'name_read1.sam'):
                            os.remove(tmp+'name_read1.sam')
                    if os.path.exists(tmp+'name_read1.bam'):
                            os.remove(tmp+'name_read1.bam')
                    if os.path.exists(tmp+'name_read1_sorted.bam'):
                            os.remove(tmp+'name_read1_sorted.bam')
                    if os.path.exists(tmp+'name_read2.sam'):
                            os.remove(tmp+'name_read2.sam')
                    if os.path.exists(tmp+'name_read2.bam'):
                            os.remove(tmp+'name_read2.bam')
                    if os.path.exists(tmp+'name_read2_sorted.bam'):
                            os.remove(tmp+'name_read2_sorted.bam')
    
        else:
            step1_9=subprocess.Popen(samtools+' sort '+tmp+'name_read1.bam '+tmp+'all',shell=True)
            step1_9.wait()
            if os.path.exists(tmp+'all.bam'):
                    if os.path.exists(tmp+'name_read1.sam'):
                            os.remove(tmp+'name_read1.sam')
                    if os.path.exists(tmp+'name_read1.bam'):
                            os.remove(tmp+'name_read1.bam')
        step2_2=subprocess.Popen(samtools+' view -h -o '+tmp+'all.sam '+tmp+'all.bam',shell=True)
        step2_2.wait()
        subprocess.Popen('cp '+tmp+'./all.sam '+ori_tmp+'/'+TAG+'_all.sam',shell=True).wait()
        if os.path.exists(tmp+'all.sam'):
            #os.remove(tmp+'all.bam')
            os.remove(tmp+'all.sam')
            #try:
            #    os.rmdir(tmp)
            #except Exception,e:
            #    pass
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    try:
    #if 1==1:
        
        sprint.cut(read1,tmp+'cut_read1.fastq',cutbp,'read1')
        if paired_end==True:
            sprint.cut(read2,tmp+'cut_read2.fastq',cutbp,'read2')
        sprint.get_baseq_cutoff(read1,tmp+'baseq.cutoff')
        
    
        TAG='genome'
        fq2sam(TAG,paired_end,tmp+'cut_read1.fastq',tmp+'cut_read2.fastq',tmp,refgenome,bwa,samtools)
    
        subprocess.Popen(samtools+' view -f4 '+tmp+'/'+TAG+'/all.bam > '+tmp+'/'+TAG+'_unmapped.sam',shell=True).wait()
        sprint.umsam2fq(tmp+'/'+TAG+'_unmapped.sam',tmp+'/'+TAG+'_unmapped.fq')
     
        if os.path.exists(refgenome+'.trans.fa'):
            TAG='transcript'
            fq2sam(TAG,'False',tmp+'/genome_unmapped.fq',read2,tmp,refgenome+'.trans.fa',bwa,samtools)
    
            subprocess.Popen(samtools+' view -f4 '+tmp+'/'+TAG+'/all.bam > '+tmp+'/'+TAG+'_unmapped.sam',shell=True).wait()
            sprint.umsam2fq(tmp+'/'+TAG+'_unmapped.sam',tmp+'/regular_unmapped.fq')    
            sprint.maskfq(tmp+'/regular_unmapped.fq','A','G')
        else:
            sprint.umsam2fq(tmp+'/'+TAG+'_unmapped.sam',tmp+'/regular_unmapped.fq')
            sprint.maskfq(tmp+'/regular_unmapped.fq','A','G')
    
    
        TAG='genome_mskAG'
        fq2sam(TAG,'False',tmp+'/regular_unmapped_A_to_G.fq',read2,tmp,refgenome+'.mskAG.fa',bwa,samtools)
    
        subprocess.Popen(samtools+' view -f4 '+tmp+'/'+TAG+'/all.bam > '+tmp+'/'+TAG+'_unmapped.sam',shell=True).wait()
        sprint.umsam2fq(tmp+'/'+TAG+'_unmapped.sam',tmp+'/'+TAG+'_unmapped.fq')    
    
        TAG='genome_mskTC'
        fq2sam(TAG,'False',tmp+'/regular_unmapped_A_to_G.fq',read2,tmp,refgenome+'.mskTC.fa',bwa,samtools)
    
        subprocess.Popen(samtools+' view -f4 '+tmp+'/'+TAG+'/all.bam > '+tmp+'/'+TAG+'_unmapped.sam',shell=True).wait()
        sprint.umsam2fq(tmp+'/'+TAG+'_unmapped.sam',tmp+'/'+TAG+'_unmapped.fq')    
        
        
        if os.path.exists(refgenome+'.trans.fa'):
            TAG='transcript_mskAG'
            fq2sam(TAG,'False',tmp+'/genome_mskAG_unmapped.fq',read2,tmp,refgenome+'.trans.fa.mskAG.fa',bwa,samtools)
    
            TAG='transcript_mskTC'
            fq2sam(TAG,'False',tmp+'/genome_mskTC_unmapped.fq',read2,tmp,refgenome+'.trans.fa.mskTC.fa',bwa,samtools)
    
        if os.path.exists(tmp+'genome_mskAG_unmapped.sam'):
                    if os.path.exists(tmp+'cut_read1.fastq'):
                            os.remove(tmp+'cut_read1.fastq')
                    if os.path.exists(tmp+'cut_read2.fastq'):
                            os.remove(tmp+'cut_read2.fastq')
                    if os.path.exists(tmp+'genome_mskAG_unmapped.fq'):
                            os.remove(tmp+'genome_mskAG_unmapped.fq')
                    if os.path.exists(tmp+'genome_mskAG_unmapped.sam'):
                            os.remove(tmp+'genome_mskAG_unmapped.sam')
                    if os.path.exists(tmp+'genome_mskTC_unmapped.fq'):
                            os.remove(tmp+'genome_mskTC_unmapped.fq')
                    if os.path.exists(tmp+'genome_mskTC_unmapped.sam'):
                            os.remove(tmp+'genome_mskTC_unmapped.sam')
                    if os.path.exists(tmp+'genome_unmapped.fq'):
                            os.remove(tmp+'genome_unmapped.fq')
                    if os.path.exists(tmp+'genome_unmapped.sam'):
                            os.remove(tmp+'genome_unmapped.sam')
                    if os.path.exists(tmp+'transcript_unmapped_A_to_G.fq'):
                            os.remove(tmp+'transcript_unmapped_A_to_G.fq')
                    if os.path.exists(tmp+'transcript_unmapped.fq'):
                            os.remove(tmp+'transcript_unmapped.fq')
                    if os.path.exists(tmp+'transcript_unmapped.sam'):
                            os.remove(tmp+'transcript_unmapped.sam')
                    if os.path.exists(tmp+'regular_unmapped.fq'):
                            os.remove(tmp+'regular_unmapped.fq')
                    if os.path.exists(tmp+'regular_unmapped_A_to_G.fq'):
                            os.remove(tmp+'regular_unmapped_A_to_G.fq')
                            
        
        if os.path.exists(refgenome+'.trans.fa'):
            sprint.recover_sam(tmp+'transcript_mskAG_all.sam',tmp+'transcript_mskAG_all.sam.rcv')
            sprint.sam2zz(tmp+'transcript_mskAG_all.sam.rcv',refgenome+'.trans.fa',tmp+'transcript_mskAG_all.zz')
            sprint.recover_sam(tmp+'transcript_mskTC_all.sam',tmp+'transcript_mskTC_all.sam.rcv')
            sprint.sam2zz(tmp+'transcript_mskTC_all.sam.rcv',refgenome+'.trans.fa',tmp+'transcript_mskTC_all.zz')
            sprint.sam2zz(tmp+'transcript_all.sam',refgenome+'.trans.fa',tmp+'transcript_all.zz')
    
        sprint.recover_sam(tmp+'genome_mskAG_all.sam',tmp+'genome_mskAG_all.sam.rcv')
        sprint.sam2zz(tmp+'genome_mskAG_all.sam.rcv',refgenome,tmp+'genome_mskAG_all.zz')
        sprint.recover_sam(tmp+'genome_mskTC_all.sam',tmp+'genome_mskTC_all.sam.rcv')
        sprint.sam2zz(tmp+'genome_mskTC_all.sam.rcv',refgenome,tmp+'genome_mskTC_all.zz')
        sprint.sam2zz(tmp+'genome_all.sam',refgenome,tmp+'genome_all.zz')
        
        if os.path.exists(refgenome+'.trans.fa'):
            sprint.dedup(tmp+'transcript_mskAG_all.zz',tmp+'transcript_mskAG_all.zz.dedup')
            sprint.dedup(tmp+'transcript_mskTC_all.zz',tmp+'transcript_mskTC_all.zz.dedup') 
            sprint.dedup(tmp+'transcript_all.zz',tmp+'transcript_all.zz.dedup') 
    
        sprint.dedup(tmp+'genome_mskAG_all.zz',tmp+'genome_mskAG_all.zz.dedup') 
        sprint.dedup(tmp+'genome_mskTC_all.zz',tmp+'genome_mskTC_all.zz.dedup') 
        sprint.dedup(tmp+'genome_all.zz',tmp+'genome_all.zz.dedup')
        
    
        if os.path.exists(refgenome+'.trans.fa'):
            sprint.mask_zz2snv(tmp+'transcript_mskAG_all.zz.dedup',tmp+'transcript_mskAG_all.zz.dedup.snv',tmp+'baseq.cutoff') 
            sprint.mask_zz2snv(tmp+'transcript_mskTC_all.zz.dedup',tmp+'transcript_mskTC_all.zz.dedup.snv',tmp+'baseq.cutoff') 
            sprint.mask_zz2snv(tmp+'transcript_all.zz.dedup',tmp+'transcript_all.zz.dedup.snv',tmp+'baseq.cutoff') 
    
        sprint.mask_zz2snv(tmp+'genome_mskAG_all.zz.dedup',tmp+'genome_mskAG_all.zz.dedup.snv',tmp+'baseq.cutoff') 
        sprint.mask_zz2snv(tmp+'genome_mskTC_all.zz.dedup',tmp+'genome_mskTC_all.zz.dedup.snv',tmp+'baseq.cutoff') 
        sprint.mask_zz2snv(tmp+'genome_all.zz.dedup',tmp+'genome_all.zz.dedup.snv',tmp+'baseq.cutoff') 
        
        
     
        if os.path.exists(refgenome+'.trans.fa'):
            sprint.transcript_locator(tmp+'transcript_mskAG_all.zz.dedup.snv',refgenome+'.trans.fa.loc', tmp+'transcript_mskAG_all.zz.dedup.snv.genome.snv')
            sprint.transcript_locator(tmp+'transcript_mskTC_all.zz.dedup.snv',refgenome+'.trans.fa.loc', tmp+'transcript_mskTC_all.zz.dedup.snv.genome.snv')
            sprint.transcript_locator(tmp+'transcript_all.zz.dedup.snv',refgenome+'.trans.fa.loc', tmp+'transcript_all.zz.dedup.snv.genome.snv')
            sprint.snv_or(tmp+'transcript_all.zz.dedup.snv.genome.snv',tmp+'genome_all.zz.dedup.snv',tmp+'regular.snv')
            sprint.snv_or(tmp+'transcript_mskTC_all.zz.dedup.snv.genome.snv',tmp+'transcript_mskAG_all.zz.dedup.snv.genome.snv',tmp+'transcript_hyper.snv')
            sprint.snv_or(tmp+'genome_mskTC_all.zz.dedup.snv',tmp+'genome_mskAG_all.zz.dedup.snv',tmp+'genome_hyper.snv')
            sprint.snv_or(tmp+'transcript_hyper.snv',tmp+'genome_hyper.snv',tmp+'hyper.snv')
        else:
            subprocess.Popen('cp '+tmp+'/genome_all.zz.dedup.snv '+tmp+'/regular.snv',shell=True).wait()
            sprint.snv_or(tmp+'genome_mskTC_all.zz.dedup.snv',tmp+'genome_mskAG_all.zz.dedup.snv',tmp+'/hyper.snv')
        
        if repeat !=False:
            sprint.annotate(tmp+'regular.snv',repeat,tmp+'regular.snv.anno')    
            sprint.seperate(tmp+'regular.snv.anno',tmp+'regular.snv.anno.alu',tmp+'regular.snv.anno.nalurp',tmp+'regular.snv.anno.nrp','Alu')
            sprint.get_snv_with_ad(tmp+'regular.snv.anno.alu',tmp+'regular.snv.anno.alu.ad2',2)
            sprint.snv_cluster(tmp+'regular.snv.anno.alu',tmp+'regular_alu.res.ad1',cluster_distance,3)
            sprint.snv_cluster(tmp+'regular.snv.anno.alu.ad2',tmp+'regular_alu.res.ad2',cluster_distance,2)
            sprint.bed_or(tmp+'regular_alu.res.ad1',tmp+'regular_alu.res.ad2',tmp+'regular_alu.res')
            sprint.snv_cluster(tmp+'regular.snv.anno.nalurp',tmp+'regular_nalurp.res',cluster_distance,5)
            sprint.snv_cluster(tmp+'regular.snv.anno.nrp',tmp+'regular_nrp.res',cluster_distance,7)
            sprint.combine_res(tmp+'regular_alu.res',tmp+'regular_nalurp.res',tmp+'regular_nrp.res',tmp+'regular.res')
    
    
            sprint.annotate(tmp+'hyper.snv',repeat,tmp+'hyper.snv.anno')    
            sprint.seperate(tmp+'hyper.snv.anno',tmp+'hyper.snv.anno.alu',tmp+'hyper.snv.anno.nalurp',tmp+'hyper.snv.anno.nrp','Alu')
            sprint.combine_res(tmp+'hyper.snv.anno.alu',tmp+'hyper.snv.anno.nalurp',tmp+'hyper.snv.anno.nrp',tmp+'hyper.snv.anno.rmsrp')
            sprint.snv_cluster(tmp+'hyper.snv.anno.rmsrp',tmp+'hyper.res_tmp',cluster_distance,5)
            sprint.o2b(tmp+'hyper.res_tmp',tmp+'hyper.res')
    
    
            #sprint.snv_cluster(tmp+'hyper.snv.anno.alu',tmp+'hyper_alu.res',cluster_distance,5)
            #sprint.snv_cluster(tmp+'hyper.snv.anno.nalurp',tmp+'hyper_nalurp.res',cluster_distance,5)
            #sprint.snv_cluster(tmp+'hyper.snv.anno.nrp',tmp+'hyper_nrp.res',cluster_distance,5)
            #sprint.combine_res(tmp+'hyper_alu.res',tmp+'hyper_nalurp.res',tmp+'hyper_nrp.res',tmp+'hyper.res')
            
    
     
        else:
            sprint.snv_cluster(tmp+'regular.snv',tmp+'regular.res_tmp',cluster_distance,5) 
            sprint.o2b(tmp+'regular.res_tmp',tmp+'regular.res') 
            sprint.snv_cluster(tmp+'hyper.snv',tmp+'hyper.res_tmp',cluster_distance,5)
            sprint.o2b(tmp+'hyper.res_tmp',tmp+'hyper.res')
        subprocess.Popen('cp '+tmp+'/regular.res '+output,shell=True).wait()
        subprocess.Popen('cp '+tmp+'/hyper.res '+output,shell=True).wait()
        sys.exit(0)
    #try:
    #    pass
    except Exception,e:
        print ''
        print 'ERROR!'
        print ''
        print e
        print ''
        help_doc()
    
    
    
    
    
    
    
 
#if __name__=='__main__':   
#    main()

