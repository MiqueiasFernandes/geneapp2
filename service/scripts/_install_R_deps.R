#####################################################################################
#####################################################################################
###############################    MASER   ##########################################
#####################################################################################

if (!require("BiocManager", quietly = TRUE))
            install.packages("BiocManager")
        BiocManager::install("maser")

#####################################################################################
#####################################################################################
###############################  3D RNASEQ  #########################################
#####################################################################################
## Install packages of dependency
###---> Install packages from Cran
cran.package.list <- c("shiny","shinydashboard","rhandsontable","shinyFiles",
                    "shinyjs","shinyBS","shinyhelper","shinyWidgets",
                    "magrittr","DT","plotly","ggplot2","eulerr",
                    "gridExtra","grid","fastcluster","rmarkdown",
                    "ggrepel","zoo","gtools")
for(i in cran.package.list){
    if(!(i %in% rownames(installed.packages()))){
        message("Installing package: ",i)
        install.packages(i)
    } else next
}
###---> Install packages from Bioconductor
bioconductor.package.list <- c("tximport","edgeR","limma","RUVSeq", "ComplexHeatmap","rhdf5")
for(i in bioconductor.package.list){
    if (!requireNamespace("BiocManager", quietly = TRUE))
        install.packages("BiocManager")
    if(!(i %in% rownames(installed.packages()))){
        message("Installing package: ",i)
        BiocManager::install(i)
    } else next
}

##################################################################################################
## use devtools R package to install ThreeDRNAseq from Github
###---> If devtools is not installed, please install
if(!requireNamespace("devtools", quietly = TRUE))
    install.packages("devtools",dependencies = TRUE)

###---> Install ThreeDRNAseq
if(!requireNamespace("ThreeDRNAseq", quietly = TRUE))
    devtools::install_github("slt666666/ThreeDRNAseq")   ########"wyguo/ThreeDRNAseq")

tryCatch( 
    {library(ThreeDRNAseq) ; message("  !!!    ✅ t3DRNASEQ INSTALED !!!") } , 
    error = function(cond){ message("   !!!   ❌ ERROR ON t3DRNASEQ INSTALL  !!! ") }
) 


## other attached packages:
##  [1] ggrepel_0.9.1               base64enc_0.1-3            
##  [3] ComplexHeatmap_1.20.0       RUVSeq_1.16.1              
##  [5] EDASeq_2.16.3               ShortRead_1.40.0           
##  [7] GenomicAlignments_1.18.1    SummarizedExperiment_1.12.0
##  [9] DelayedArray_0.8.0          matrixStats_0.54.0         
## [11] Rsamtools_1.34.1            GenomicRanges_1.34.0       
## [13] GenomeInfoDb_1.18.2         Biostrings_2.50.2          
## [15] XVector_0.22.0              IRanges_2.16.0             
## [17] S4Vectors_0.20.1            BiocParallel_1.16.6        
## [19] Biobase_2.42.0              BiocGenerics_0.28.0        
## [21] edgeR_3.24.3                limma_3.38.3               
## [23] tximport_1.10.1             rmarkdown_2.14             
## [25] fastcluster_1.2.3           gridExtra_2.3              
## [27] eulerr_6.1.1                plotly_4.10.0              
## [29] ggplot2_3.3.6               DT_0.22                    
## [31] magrittr_2.0.3              shinyWidgets_0.6.4         
## [33] shinyhelper_0.3.2           shinyBS_0.61.1             
## [35] shinyjs_2.1.0               shinyFiles_0.9.1           
## [37] rhandsontable_0.3.8         shinydashboard_0.7.2       
## [39] shiny_1.7.1  
