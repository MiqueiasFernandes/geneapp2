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
    devtools::install_github("wyguo/ThreeDRNAseq")

tryCatch( 
    {library(ThreeDRNAseq) ; message("  !!!    ✅ t3DRNASEQ INSTALED !!!") } , 
    error = function(cond){ message("   !!!   ❌ ERROR ON t3DRNASEQ INSTALL  !!! ") }
) 
