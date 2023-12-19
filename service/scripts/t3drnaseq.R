### ---> ThreeDRNAseq R package
library(ThreeDRNAseq)

### ---> Denpendency R package
library(tximport)
library(edgeR)
library(limma)
library(RUVSeq)
library(eulerr)
library(gridExtra)
library(grid)
library(ComplexHeatmap)
library(ggplot2)
library(ggrepel)

options(stringsAsFactors = F)

args <- commandArgs(trailingOnly = TRUE)

projects <- args[[1]]
project <- args[[2]]
inputs <- paste0(projects, "/", project, "/", "inputs")
results <- paste0(projects, "/", project, "/", "results")
job <- args[[3]]
ctrl <- args[[4]]
trt <- args[[5]]

label1 <- ctrl
label2 <- trt
tmp_dir <- paste0(inputs, "/", "t3drnaseq_tmp")
qnt_dir <- paste0(inputs)

show(paste("ARGS: ", label1, label2, tmp_dir, qnt_dir, args))
setwd(tmp_dir)


if ("t3drnaseq executado." %in% readLines(paste0(results, "/status.txt"))) {
    show("skiping previous 3drnaseq run")
} else {
    ## save to object
    DDD.data <- list()
    ################################################################################
    ## ----->> Set folders to read and save results
    data.folder <- file.path(getwd(), "data") # for .RData format results
    result.folder <- file.path(getwd(), "result") # for 3D analysis results in csv files
    figure.folder <- file.path(getwd(), "figure") # for figures
    report.folder <- file.path(getwd(), "report")

    DDD.data$data.folder <- data.folder
    DDD.data$result.folder <- result.folder
    DDD.data$figure.folder <- figure.folder
    DDD.data$report.folder <- report.folder

    if (!file.exists(data.folder)) {
        dir.create(path = data.folder, recursive = T)
    }
    if (!file.exists(result.folder)) {
        dir.create(path = result.folder, recursive = T)
    }
    if (!file.exists(figure.folder)) {
        dir.create(path = figure.folder, recursive = T)
    }
    if (!file.exists(report.folder)) {
        dir.create(path = report.folder, recursive = T)
    }

    ### Set the input data folder
    ## ----->> folder of input files
    input.folder <- tmp_dir
    quant.folder <- qnt_dir

    ################################################################################
    ## ----->> parameters of tximport to generate read counts and TPMs
    quant_method <- "salmon" # abundance generator
    tximport_method <- "lengthScaledTPM" # method to generate expression in tximport

    ################################################################################
    ## ----->> parameters for data pre-processing
    ### has sequencign replicates?
    has_srep <- F

    ### parameter for low expression filters
    cpm_cut <- 1
    cpm_samples_n <- 3

    ### parameter for batch effect estimation
    has_batcheffect <- T
    RUVseq_method <- "RUVr" # RUVseq_method is one of "RUVr", "RUVs" and "RUVg"

    ### data normalisation parameter
    norm_method <- "TMM" ## norm_method is one of "TMM","RLE" and "upperquartile"

    ################################################################################
    ## ----->> parameters for 3D analysis
    pval_adj_method <- "BH"
    pval_cut <- 0.01
    l2fc_cut <- 1
    DE_pipeline <- "limma"
    deltaPS_cut <- 0.1
    DAS_pval_method <- "F-test"

    ################################################################################
    ## ----->> heatmap
    dist_method <- "euclidean"
    cluster_method <- "ward.D"
    cluster_number <- 10

    ################################################################################
    ## ----->> TSIS
    TSISorisokTSP <- "isokTSP"
    TSIS_method_intersection <- method_intersection <- "mean"
    TSIS_spline_df <- spline_df <- NULL
    TSIS_prob_cut <- 0.5
    TSIS_diff_cut <- 1
    TSIS_adj_pval_cut <- 0.05
    TSIS_time_point_cut <- 1
    TSIS_cor_cut <- 0

    ################################################################################
    ## ----->> Meta table includes sample information, e.g. conditions, bio-reps, seq-reps, abundance paths, etc.
    metatable <- read.csv(file.path(results, "experimental_design.csv"))
    ## select the columns of experimental design
    factor_col <- c("FACTOR")
    brep_col <- "SAMPLE"
    quant_col <- "FOLDER"
    srep_col <- "seq_rep"

    ## arrange information in the metatable
    metatable$label <- as.vector(interaction(metatable[, factor_col]))
    metatable$sample.name <- as.vector(interaction(metatable[, c(factor_col, brep_col)]))
    metatable$quant.folder <- file.path(
        quant.folder, metatable[, quant_col],
        ifelse(quant_method == "salmon", "quant.sf", "abundance.h5")
    )
    show(metatable)

    ## ----->> Transcript-gene association mapping
    mapping <- read.csv(file.path(getwd(), "transcript_gene_mapping.csv"))
    mapping <- data.frame(as.matrix(mapping), stringsAsFactors = F)
    rownames(mapping) <- mapping$TXNAME
    show(paste("Genes importados: ", length(unique(mapping$GENEID))))
    show(paste("Transcript importados: ", length(unique(mapping$TXNAME))))

    show("==========> Read files      => OK")

    z = strsplit(args[[6]], " ")[[1]]
    for (x in z) { 
        p=gsub(":.*", "", x)
        v=gsub(".*:", "", x)
        if (nchar(p) > 1 && nchar(v) > 0) {
            is_str = grepl("@", v)
            if (is_str) {
                v <- gsub("@", "", v)
                show(paste(" ====>  Assigin STR ", p, " <- ",  v))
            } else {
                v <- as.double(v)
                show(paste(" ====>  Assigin NUMBER ", p, " <- ",  v))
            }
            assign(p, v)
        }
    }


    ################################################################################
    ## ----->> Generate gene expression
    ##
    txi_genes <- tximport(metatable$quant.folder,
        dropInfReps = T,
        type = quant_method, tx2gene = mapping,
        countsFromAbundance = tximport_method
    )

    ## give colunames to the datasets
    colnames(txi_genes$counts) <-
        colnames(txi_genes$abundance) <-
        colnames(txi_genes$length) <- metatable$sample.name

    ## save the data
    write.csv(txi_genes$counts, file = paste0(result.folder, "/counts_genes.csv"))
    write.csv(txi_genes$abundance, file = paste0(result.folder, "/TPM_genes.csv"))
    save(txi_genes, file = paste0(data.folder, "/txi_genes.RData"))

    ################################################################################
    ## ----->> Generate transcripts expression
    txi_trans <- tximport(metatable$quant.folder,
        type = quant_method, tx2gene = NULL,
        countsFromAbundance = tximport_method,
        txOut = T, dropInfReps = T
    )

    ## give colunames to the datasets
    colnames(txi_trans$counts) <-
        colnames(txi_trans$abundance) <-
        colnames(txi_trans$length) <- metatable$sample.name

    ## save the data
    write.csv(txi_trans$counts, file = paste0(result.folder, "/counts_trans.csv"))
    write.csv(txi_trans$abundance, file = paste0(result.folder, "/TPM_trans.csv"))
    save(txi_trans, file = paste0(data.folder, "/txi_trans.RData"))

    ################################################################################
    ## extract gene and transcript read counts
    genes_counts <- txi_genes$counts
    trans_counts <- txi_trans$counts
    trans_TPM <- txi_trans$abundance


    show("==========> Run tximport    => OK")

    ## If no sequencing replicates, genes_counts and trans_counts remain the same by
    if (has_srep) {
        idx <- paste0(metatable$label, ".", metatable[, brep_col])
        genes_counts <- sumarrays(genes_counts, group = idx)
        trans_counts <- sumarrays(trans_counts, group = idx)
        metatable_new <- metatable[metatable[, srep_col] == metatable[, srep_col][1], ]
    } else {
        metatable_new <- metatable
    }

    show("==========> Step 1: Merge sequencing replicates    => OK")


    ################################################################################
    ## ----->> Do the filters
    target_high <- low.expression.filter(
        abundance = trans_counts,
        mapping = mapping,
        abundance.cut = cpm_cut,
        sample.n = cpm_samples_n,
        unit = "counts",
        Log = F
    )
    ## save expressed genes and transcripts
    save(target_high, file = paste0(data.folder, "/target_high.RData"))

    ################################################################################
    ## ----->> Mean-variance plot
    ## transcript level

    counts.raw <- trans_counts[rowSums(trans_counts > 0) > 0, ]
    counts.filtered <- trans_counts[target_high$trans_high, ]
    mv.trans <- check.mean.variance(
        counts.raw = counts.raw,
        counts.filtered = counts.filtered,
        condition = metatable_new$label
    )
    ### make plot
    fit.raw <- mv.trans$fit.raw
    fit.filtered <- mv.trans$fit.filtered
    mv.trans.plot <- function() {
        par(mfrow = c(1, 2))
        plotMeanVariance(
            x = fit.raw$sx, y = fit.raw$sy,
            l = fit.raw$l, lwd = 2, fit.line.col = "gold", col = "black"
        )
        title("\n\nRaw counts (transcript level)")
        plotMeanVariance(
            x = fit.filtered$sx, y = fit.filtered$sy,
            l = fit.filtered$l, lwd = 2, col = "black"
        )
        title("\n\nFiltered counts (transcript level)")
        lines(fit.raw$l, col = "gold", lty = 4, lwd = 2)
        legend("topright",
            col = c("red", "gold"), lty = c(1, 4), lwd = 3,
            legend = c("low-exp removed", "low-exp kept")
        )
    }
    mv.trans.plot()

    ### save to figure folder
    png(
        filename = paste0(figure.folder, "/Transcript mean-variance trend.png"),
        width = 25 / 2.54, height = 12 / 2.54, units = "in", res = 300
    )
    mv.trans.plot()
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Transcript mean-variance trend.pdf"),
        width = 25 / 2.54, height = 12 / 2.54
    )
    mv.trans.plot()
    dev.off()

    ################################################################################
    ## gene level
    counts.raw <- genes_counts[rowSums(genes_counts > 0) > 0, ]
    counts.filtered <- genes_counts[target_high$genes_high, ]
    mv.genes <- check.mean.variance(
        counts.raw = counts.raw,
        counts.filtered = counts.filtered,
        condition = metatable_new$label
    )
    ### make plot
    fit.raw <- mv.genes$fit.raw
    fit.filtered <- mv.genes$fit.filtered
    mv.genes.plot <- function() {
        par(mfrow = c(1, 2))
        plotMeanVariance(
            x = fit.raw$sx, y = fit.raw$sy,
            l = fit.raw$l, lwd = 2, fit.line.col = "gold", col = "black"
        )
        title("\n\nRaw counts (gene level)")
        plotMeanVariance(
            x = fit.filtered$sx, y = fit.filtered$sy,
            l = fit.filtered$l, lwd = 2, col = "black"
        )
        title("\n\nFiltered counts (gene level)")
        lines(fit.raw$l, col = "gold", lty = 4, lwd = 2)
        legend("topright",
            col = c("red", "gold"), lty = c(1, 4), lwd = 3,
            legend = c("low-exp removed", "low-exp kept")
        )
    }
    mv.genes.plot()

    ### save to figure folder
    png(
        filename = paste0(figure.folder, "/Gene mean-variance trend.png"),
        width = 25 / 2.54, height = 12 / 2.54, units = "in", res = 300
    )
    mv.genes.plot()
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Gene mean-variance trend.pdf"),
        width = 25 / 2.54, height = 12 / 2.54
    )
    mv.genes.plot()
    dev.off()

    show("==========> Step 2: Filter low expression transcripts/genes   => OK")


    ################################################################################
    ## ----->> trans level
    data2pca <- trans_counts[target_high$trans_high, ]
    dge <- DGEList(counts = data2pca)
    dge <- calcNormFactors(dge)
    data2pca <- t(counts2CPM(obj = dge, Log = T))
    dim1 <- "PC1"
    dim2 <- "PC2"
    ellipse.type <- "polygon" # ellipse.type=c("none","ellipse","polygon")

    ## --All Bio-reps plots
    groups <- metatable_new[, brep_col] ## colour on biological replicates
    # groups <- metatable_new$label ## colour on condtions
    g <- plotPCAind(
        data2pca = data2pca, dim1 = dim1, dim2 = dim2,
        groups = groups, plot.title = "Transcript PCA: bio-reps",
        ellipse.type = ellipse.type,
        add.label = T, adj.label = F
    )

    g

    ### save to figure
    png(
        filename = paste0(figure.folder, "/Transcript PCA Bio-reps.png"),
        width = 15 / 2.54, height = 13 / 2.54, units = "in", res = 300
    )
    print(g)
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Transcript PCA Bio-reps.pdf"),
        width = 15 / 2.54, height = 13 / 2.54
    )
    print(g)
    dev.off()

    ##################################################
    ## --average expression plot
    groups <- metatable_new[, brep_col]
    data2pca.ave <- rowmean(data2pca, metatable_new$label, reorder = F)
    groups <- unique(metatable_new$label)
    g <- plotPCAind(
        data2pca = data2pca.ave, dim1 = "PC1", dim2 = "PC2",
        groups = groups, plot.title = "Transcript PCA: average expression",
        ellipse.type = "none", add.label = T, adj.label = F
    )

    g

    ### save to figure
    png(
        filename = paste0(figure.folder, "/Transcript PCA average expression.png"),
        width = 15 / 2.54, height = 13 / 2.54, units = "in", res = 300
    )
    print(g)
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Transcript PCA average expression.pdf"),
        width = 15 / 2.54, height = 13 / 2.54
    )
    print(g)
    dev.off()


    ################################################################################
    ## ----->> genes level
    data2pca <- genes_counts[target_high$genes_high, ]
    dge <- DGEList(counts = data2pca)
    dge <- calcNormFactors(dge)
    data2pca <- t(counts2CPM(obj = dge, Log = T))
    dim1 <- "PC1"
    dim2 <- "PC2"
    ellipse.type <- "polygon" # ellipse.type=c("none","ellipse","polygon")

    ## --All Bio-reps plots

    groups <- metatable_new[, brep_col] ## colour on biological replicates
    # groups <- metatable_new$label ## colour on condtions
    g <- plotPCAind(
        data2pca = data2pca, dim1 = dim1, dim2 = dim2,
        groups = groups, plot.title = "genescript PCA: bio-reps",
        ellipse.type = ellipse.type,
        add.label = T, adj.label = F
    )

    g

    ### save to figure
    png(
        filename = paste0(figure.folder, "/Gene PCA Bio-reps.png"),
        width = 15 / 2.54, height = 13 / 2.54, units = "in", res = 300
    )
    print(g)
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Gene PCA Bio-reps.pdf"),
        width = 15 / 2.54, height = 13 / 2.54
    )
    print(g)
    dev.off()

    ##################################################
    ## --average expression plot
    rownames(data2pca) <- gsub("_", ".", rownames(data2pca))
    groups <- metatable_new[, brep_col]
    data2pca.ave <- rowmean(data2pca, metatable_new$label, reorder = F)
    groups <- unique(metatable_new$label)
    g <- plotPCAind(
        data2pca = data2pca.ave, dim1 = "PC1", dim2 = "PC2",
        groups = groups, plot.title = "genescript PCA: average expression",
        ellipse.type = "none", add.label = T, adj.label = F
    )

    g

    ### save to figure
    png(
        filename = paste0(figure.folder, "/Gene PCA average expression.png"),
        width = 15 / 2.54, height = 13 / 2.54, units = "in", res = 300
    )
    print(g)
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Gene PCA average expression.pdf"),
        width = 15 / 2.54, height = 13 / 2.54
    )
    print(g)
    dev.off()


    show("==========> Step 3: Principal component analysis (PCA)   => OK")

    design <- condition2design(
        condition = metatable_new$label,
        batch.effect = NULL
    )

    ################################################################################
    ## ----->> trans level
    trans_batch <- remove.batch(
        read.counts = trans_counts[target_high$trans_high, ],
        condition = metatable_new$label,
        design = design,
        contrast = NULL,
        group = metatable_new$label,
        method = RUVseq_method
    )
    save(trans_batch, file = paste0(data.folder, "/trans_batch.RData"))

    ################################################################################
    ## ----->> genes level
    genes_batch <- remove.batch(
        read.counts = genes_counts[target_high$genes_high, ],
        condition = metatable_new$label,
        design = design,
        contrast = NULL,
        group = metatable_new$label,
        method = RUVseq_method
    )
    save(genes_batch, file = paste0(data.folder, "/genes_batch.RData"))


    ################################################################################
    ## DO the PCA again
    ################################################################################

    ## ----->> trans level
    data2pca <- trans_batch$normalizedCounts[target_high$trans_high, ]
    dge <- DGEList(counts = data2pca)
    dge <- calcNormFactors(dge)
    data2pca <- t(counts2CPM(obj = dge, Log = T))
    dim1 <- "PC1"
    dim2 <- "PC2"
    ellipse.type <- "polygon" # ellipse.type=c("none","ellipse","polygon")

    ## --All Bio-reps plots
    groups <- metatable_new[, brep_col] ## colour on biological replicates
    # groups <- metatable_new$label ## colour on condtions
    g <- plotPCAind(
        data2pca = data2pca, dim1 = dim1, dim2 = dim2,
        groups = groups, plot.title = "Transcript PCA: bio-reps",
        ellipse.type = ellipse.type,
        add.label = T, adj.label = F
    )

    g

    ### save to figure
    png(
        filename = paste0(figure.folder, "/Transcript PCA batch effect removed Bio-reps.png"),
        width = 15 / 2.54, height = 13 / 2.54, units = "in", res = 300
    )
    print(g)
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Transcript PCA batch effect removed Bio-reps.pdf"),
        width = 15 / 2.54, height = 13 / 2.54
    )
    print(g)
    dev.off()

    ##################################################
    ## --average expression plot
    groups <- metatable_new[, brep_col]
    data2pca.ave <- rowmean(data2pca, metatable_new$label, reorder = F)
    groups <- unique(metatable_new$label)
    g <- plotPCAind(
        data2pca = data2pca.ave, dim1 = "PC1", dim2 = "PC2",
        groups = groups, plot.title = "Transcript PCA: average expression",
        ellipse.type = "none", add.label = T, adj.label = F
    )

    g

    ### save to figure
    png(
        filename = paste0(figure.folder, "/Transcript PCA batch effect removed average expression.png"),
        width = 15 / 2.54, height = 13 / 2.54, units = "in", res = 300
    )
    print(g)
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Transcript PCA batch effect removed average expression.pdf"),
        width = 15 / 2.54, height = 13 / 2.54
    )
    print(g)
    dev.off()


    ################################################################################
    ## ----->> genes level
    data2pca <- genes_batch$normalizedCounts[target_high$genes_high, ]
    dge <- DGEList(counts = data2pca)
    dge <- calcNormFactors(dge)
    data2pca <- t(counts2CPM(obj = dge, Log = T))
    dim1 <- "PC1"
    dim2 <- "PC2"
    ellipse.type <- "polygon" # ellipse.type=c("none","ellipse","polygon")

    ## --All Bio-reps plots
    rownames(data2pca) <- gsub("_", ".", rownames(data2pca))
    groups <- metatable_new[, brep_col] ## colour on biological replicates
    # groups <- metatable_new$label ## colour on condtions
    g <- plotPCAind(
        data2pca = data2pca, dim1 = dim1, dim2 = dim2,
        groups = groups, plot.title = "genescript PCA: bio-reps",
        ellipse.type = ellipse.type,
        add.label = T, adj.label = F
    )

    g

    ### save to figure
    png(
        filename = paste0(figure.folder, "/Gene PCA batch effect removed Bio-reps.png"),
        width = 15 / 2.54, height = 13 / 2.54, units = "in", res = 300
    )
    print(g)
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Gene PCA batch effect removed Bio-reps.pdf"),
        width = 15 / 2.54, height = 13 / 2.54
    )
    print(g)
    dev.off()

    ##################################################
    ## --average expression plot
    rownames(data2pca) <- gsub("_", ".", rownames(data2pca))
    groups <- metatable_new[, brep_col]
    data2pca.ave <- rowmean(data2pca, metatable_new$label, reorder = F)
    groups <- unique(metatable_new$label)
    g <- plotPCAind(
        data2pca = data2pca.ave, dim1 = "PC1", dim2 = "PC2",
        groups = groups, plot.title = "genescript PCA: average expression",
        ellipse.type = "none", add.label = T, adj.label = F
    )

    g

    ### save to figure
    png(
        filename = paste0(figure.folder, "/Gene PCA batch effect removed average expression.png"),
        width = 15 / 2.54, height = 13 / 2.54, units = "in", res = 300
    )
    print(g)
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Gene PCA batch effect removed average expression.pdf"),
        width = 15 / 2.54, height = 13 / 2.54
    )
    print(g)
    dev.off()


    show("==========> Step 4: Batch effect estimation   => OK")



    ################################################################################
    ## ----->> trans level
    dge <- DGEList(
        counts = trans_counts[target_high$trans_high, ],
        group = metatable_new$label,
        genes = mapping[target_high$trans_high, ]
    )
    trans_dge <- suppressWarnings(calcNormFactors(dge, method = norm_method))
    save(trans_dge, file = paste0(data.folder, "/trans_dge.RData"))

    ################################################################################
    ## ----->> genes level
    dge <- DGEList(
        counts = genes_counts[target_high$genes_high, ],
        group = metatable_new$label
    )
    genes_dge <- suppressWarnings(calcNormFactors(dge, method = norm_method))
    save(genes_dge, file = paste0(data.folder, "/genes_dge.RData"))

    ################################################################################
    ## ----->> distribution plot
    sample.name <- paste0(metatable_new$label, ".", metatable_new[, brep_col])
    condition <- metatable_new$label

    ### --- trans level
    data.before <- trans_counts[target_high$trans_high, ]
    data.after <- counts2CPM(obj = trans_dge, Log = T)
    g <- boxplotNormalised(
        data.before = data.before,
        data.after = data.after,
        condition = condition,
        sample.name = sample.name
    )
    do.call(grid.arrange, g)

    ### save to figure
    png(
        filename = paste0(figure.folder, "/Transcript expression distribution.png"),
        width = 20 / 2.54, height = 20 / 2.54, units = "in", res = 300
    )
    do.call(grid.arrange, g)
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Transcript expression distribution.pdf"),
        width = 20 / 2.54, height = 20 / 2.54
    )
    do.call(grid.arrange, g)
    dev.off()

    ### --- genes level
    data.before <- genes_counts[target_high$genes_high, ]
    data.after <- counts2CPM(obj = genes_dge, Log = T)
    g <- boxplotNormalised(
        data.before = data.before,
        data.after = data.after,
        condition = condition,
        sample.name = sample.name
    )
    do.call(grid.arrange, g)

    ### save to figure
    png(
        filename = paste0(figure.folder, "/Gene expression distribution.png"),
        width = 20 / 2.54, height = 20 / 2.54, units = "in", res = 300
    )
    do.call(grid.arrange, g)
    dev.off()

    pdf(
        file = paste0(figure.folder, "/Gene expression distribution.pdf"),
        width = 20 / 2.54, height = 20 / 2.54
    )
    do.call(grid.arrange, g)
    dev.off()



    show("==========> Step 5: Data normalization   => OK")

    RNAseq_info <- data.frame(
        Description = c(
            "Raw transcripts",
            "Raw genes",
            "Samples",
            "Samples after merging seq-reps",
            "Condition of interest",
            "CPM cut-off",
            "Min samples to CPM cut-off",
            "Expressed transcripts",
            "Expressed genes"
        ),
        Number = c(
            length(mapping$TXNAME),
            length(unique(mapping$GENEID)),
            nrow(metatable),
            nrow(metatable_new),
            length(unique(metatable$label)),
            cpm_cut,
            cpm_samples_n,
            length(target_high$trans_high),
            length(target_high$genes_high)
        )
    )
    DDD.data$RNAseq_info <- RNAseq_info

    RNAseq_info

    contrast_uniq <- paste0(label1, "-", label2)
    contrast_pw <- c(contrast_uniq)

    ## ----->> group mean contrast groups
    contrast_mean <- c()

    ## ----->> group differences contrast groups
    contrast_pgdiff <- c()

    ## ----->> put together
    contrast <- unique(c(contrast_pw, contrast_mean, contrast_pgdiff))

    DDD.data$contrast_pw <- contrast_pw
    DDD.data$contrast_mean <- contrast_mean
    DDD.data$contrast_pgdiff <- contrast_pgdiff
    DDD.data$contrast <- contrast


    show("==========> Step 1: Set contrast group   => OK")


    batch.effect <- genes_batch$W
    # batch.effect <- NULL ## if has no batch effects
    design <- condition2design(
        condition = metatable_new$label,
        batch.effect = batch.effect
    )

    ################################################################################
    if (DE_pipeline == "limma") {
        ## ----->> limma pipeline
        genes_3D_stat <- limma.pipeline(
            dge = genes_dge,
            design = design,
            deltaPS = NULL,
            contrast = contrast,
            diffAS = F,
            adjust.method = pval_adj_method
        )
    }

    if (DE_pipeline == "glmQL") {
        ## ----->> edgeR glmQL pipeline
        genes_3D_stat <- edgeR.pipeline(
            dge = genes_dge,
            design = design,
            deltaPS = NULL,
            contrast = contrast,
            diffAS = F,
            method = "glmQL",
            adjust.method = pval_adj_method
        )
    }

    if (DE_pipeline == "glm") {
        ## ----->> edgeR glm pipeline
        genes_3D_stat <- edgeR.pipeline(
            dge = genes_dge,
            design = design,
            deltaPS = NULL,
            contrast = contrast,
            diffAS = F,
            method = "glm",
            adjust.method = pval_adj_method
        )
    }
    ## save results
    DDD.data$genes_3D_stat <- genes_3D_stat

    show("==========> Step 2: DE genes  => OK")

    ################################################################################
    ## ----->> generate deltaPS
    deltaPS <- transAbundance2PS(
        transAbundance = txi_trans$abundance[target_high$trans_high, ],
        PS = NULL,
        contrast = contrast,
        condition = metatable$label,
        mapping = mapping[target_high$trans_high, ]
    )

    DDD.data$PS <- PS <- deltaPS$PS
    DDD.data$deltaPS <- deltaPS <- deltaPS$deltaPS


    ################################################################################
    ## ----->> DAS genes,DE and DTU transcripts
    batch.effect <- genes_batch$W
    # batch.effect <- NULL ## if has no batch effects
    design <- condition2design(
        condition = metatable_new$label,
        batch.effect = batch.effect
    )

    ################################################################################
    if (DE_pipeline == "limma") {
        ## ----->> limma pipeline
        trans_3D_stat <- limma.pipeline(
            dge = trans_dge,
            design = design,
            deltaPS = deltaPS,
            contrast = contrast,
            diffAS = T,
            adjust.method = pval_adj_method
        )
    }

    if (DE_pipeline == "glmQL") {
        ## ----->> edgeR glmQL pipeline
        trans_3D_stat <- edgeR.pipeline(
            dge = trans_dge,
            design = design,
            deltaPS = deltaPS,
            contrast = contrast,
            diffAS = T,
            method = "glmQL",
            adjust.method = pval_adj_method
        )
    }

    if (DE_pipeline == "glm") {
        ## ----->> edgeR glm pipeline
        trans_3D_stat <- edgeR.pipeline(
            dge = trans_dge,
            design = design,
            deltaPS = deltaPS,
            contrast = contrast,
            diffAS = T,
            method = "glm",
            adjust.method = pval_adj_method
        )
    }
    ## save results
    DDD.data$trans_3D_stat <- trans_3D_stat

    show("==========> Step 3: DAS genes, DE and DTU transcripts => OK")

    ################################################################################
    ## ----->> Summary DE genes
    DE_genes <- summaryDEtarget(
        stat = genes_3D_stat$DE.stat,
        cutoff = c(
            adj.pval = pval_cut,
            log2FC = l2fc_cut
        )
    )
    DDD.data$DE_genes <- DE_genes

    ################################################################################
    ## summary DAS genes, DE and DTU trans
    ## ----->> DE trans
    DE_trans <- summaryDEtarget(
        stat = trans_3D_stat$DE.stat,
        cutoff = c(
            adj.pval = pval_cut,
            log2FC = l2fc_cut
        )
    )
    DDD.data$DE_trans <- DE_trans

    ## ----->> DAS genes


    if (DAS_pval_method == "F-test") {
        DAS.stat <- trans_3D_stat$DAS.F.stat
    } else {
        DAS.stat <- trans_3D_stat$DAS.Simes.stat
    }

    summaryDAStarget2 <- function(stat, lfc, cutoff = c(adj.pval = 0.01, deltaPS = 0.1)) {
        names(cutoff) <- c("adj.pval", "deltaPS")
        lfc <- lfc[which(lfc$target %in% stat$target), ]
        stat <- merge(stat, lfc)
        stat$up.down <- NULL
        idx <- NULL
        stat <- stat[idx, ]
        return(stat)
    }

    if (is.null(DAS.stat)) {
        summaryDAStarget <- summaryDAStarget2
        warning(" !!!!! NO DAS FOUND !!!!!!")
    } else {
        lfc <- genes_3D_stat$DE.lfc
        lfc <- reshape2::melt(as.matrix(lfc))
        colnames(lfc) <- c("target", "contrast", "log2FC")


        DAS_genes <- summaryDAStarget(
            stat = DAS.stat,
            lfc = lfc,
            cutoff = c(pval_cut, deltaPS_cut)
        )


        DDD.data$DAS_genes <- DAS_genes

        ## ----->> DTU trans
        lfc <- trans_3D_stat$DE.lfc
        lfc <- reshape2::melt(as.matrix(lfc))
        colnames(lfc) <- c("target", "contrast", "log2FC")
        DTU_trans <- summaryDAStarget(
            stat = trans_3D_stat$DTU.stat,
            lfc = lfc, cutoff = c(
                adj.pval = pval_cut,
                deltaPS = deltaPS_cut
            )
        )
        DDD.data$DTU_trans <- DTU_trans

        ################################################################################
        ## save csv
        write.csv(DE_genes, file = paste0(result.folder, "/DE genes.csv"), row.names = F)
        write.csv(DAS_genes, file = paste0(result.folder, "/DAS genes.csv"), row.names = F)
        write.csv(DE_trans, file = paste0(result.folder, "/DE transcripts.csv"), row.names = F)
        write.csv(DTU_trans, file = paste0(result.folder, "/DTU transcripts.csv"), row.names = F)

        ################################################################################
        ## ----->> target numbers
        DDD_numbers <- summary3Dnumber(
            DE_genes = DE_genes,
            DAS_genes = DAS_genes,
            DE_trans = DE_trans,
            DTU_trans = DTU_trans,
            contrast = contrast
        )
        DDD_numbers
        write.csv(DDD_numbers,
            file = paste0(result.folder, "/DE DAS DTU numbers.csv"),
            row.names = F
        )
        DDD.data$DDD_numbers <- DDD_numbers
        ################################################################################
        ## ----->> DE vs DAS
        DEvsDAS_results <- DEvsDAS(
            DE_genes = DE_genes,
            DAS_genes = DAS_genes,
            contrast = contrast
        )
        DEvsDAS_results
        DDD.data$DEvsDAS_results <- DEvsDAS_results
        write.csv(DEvsDAS_results,
            file = paste0(result.folder, "/DE vs DAS gene number.csv"),
            row.names = F
        )


        ################################################################################
        ## ----->> DE vs DTU
        DEvsDTU_results <- DEvsDTU(
            DE_trans = DE_trans,
            DTU_trans = DTU_trans,
            contrast = contrast
        )
        DEvsDTU_results
        DDD.data$DEvsDTU_results <- DEvsDTU_results
        write.csv(DEvsDTU_results, file = paste0(result.folder, "/DE vs DTU transcript number.csv"), row.names = F)


        show("==========> Step 4 Result summary")


        ################################################################################
        ## ----->> DE genes
        idx <- factor(DE_genes$contrast, levels = contrast)
        targets <- split(DE_genes, idx)
        data2plot <- lapply(contrast, function(i) {
            if (nrow(targets[[i]]) == 0) {
                x <- data.frame(contrast = i, regulation = c("down-regulated", "up-regulated"), number = 0)
            } else {
                x <- data.frame(contrast = i, table(targets[[i]]$up.down))
                colnames(x) <- c("contrast", "regulation", "number")
            }
            x
        })
        data2plot <- do.call(rbind, data2plot)
        g.updown <- plotUpdown(data2plot, plot.title = "DE genes", contrast = contrast)
        print(g.updown)

        ### save to figure
        png(paste0(figure.folder, "/DE genes up and down regulation numbers.png"),
            width = length(contrast) * 5 / 2.54, 10 / 2.54, units = "in", res = 300
        )
        print(g.updown)
        dev.off()

        pdf(paste0(figure.folder, "/DE genes up and down regulation numbers.pdf"),
            width = length(contrast) * 5 / 2.54, 10 / 2.54
        )
        print(g.updown)
        dev.off()

        ################################################################################
        ## ----->> DE trans
        idx <- factor(DE_trans$contrast, levels = contrast)
        targets <- split(DE_trans, idx)
        data2plot <- lapply(contrast, function(i) {
            if (nrow(targets[[i]]) == 0) {
                x <- data.frame(contrast = i, regulation = c("down-regulated", "up-regulated"), number = 0)
            } else {
                x <- data.frame(contrast = i, table(targets[[i]]$up.down))
                colnames(x) <- c("contrast", "regulation", "number")
            }
            x
        })
        data2plot <- do.call(rbind, data2plot)
        g.updown <- plotUpdown(data2plot, plot.title = "DE trans", contrast = contrast)
        print(g.updown)

        ### save to figure
        png(paste0(figure.folder, "/DE transcripts up and down regulation numbers.png"),
            width = length(contrast) * 5 / 2.54, 10 / 2.54, units = "in", res = 300
        )
        print(g.updown)
        dev.off()

        pdf(paste0(figure.folder, "/DE transcripts up and down regulation numbers.pdf"),
            width = length(contrast) * 5 / 2.54, 10 / 2.54
        )
        print(g.updown)
        dev.off()




        top.n <- 10
        size <- 1
        col0 <- "black"
        col1 <- "red"
        idx <- c("DE genes", "DAS genes", "DE transcripts", "DTU transcripts")
        title.idx <- c(
            paste0(
                "Volcano plot: DE genes (Low expression filtered; \nAdjusted p<",
                pval_cut, "; |L2FC|>=", l2fc_cut, "; Labels: top ",
                top.n, " distance to (0,0))"
            ),
            paste0(
                "Volcano plot: DAS genes (Low expression filtered; \nAdjusted p<",
                pval_cut, "; |MaxdeltaPS|>=", deltaPS_cut, "; Labels: top ",
                top.n, " distance to (0,0))"
            ),
            paste0(
                "Volcano plot: DE transcripts (Low expression filtered; \nAdjusted p<",
                pval_cut, "; |L2FC|>=", l2fc_cut, "; Labels: top ",
                top.n, " distance to (0,0))"
            ),
            paste0(
                "Volcano plot: DTU transcripts (Low expression filtered; \nAdjusted p<",
                pval_cut, "; |deltaPS|>=", deltaPS_cut, "; Labels: top ",
                top.n, " distance to (0,0))"
            )
        )
        names(title.idx) <- idx
        g <- lapply(idx, function(i) {
            if (i == "DE genes") {
                DDD.stat <- genes_3D_stat$DE.stat
                data2plot <- data.frame(
                    target = DDD.stat$target,
                    contrast = DDD.stat$contrast,
                    x = DDD.stat$log2FC,
                    y = -log10(DDD.stat$adj.pval)
                )
                data2plot$significance <- "Not significant"
                data2plot$significance[DDD.stat$adj.pval < pval_cut &
                    abs(DDD.stat$log2FC) >= l2fc_cut] <- "Significant"
                q <- plotVolcano(
                    data2plot = data2plot, xlab = "log2FC of genes", ylab = "-log10(FDR)",
                    title = title.idx[i],
                    col0 = col0, col1 = col1, size = size, top.n = top.n
                )
            }

            if (i == "DAS genes") {
                if (DAS_pval_method == "F-test") {
                    DDD.stat <- trans_3D_stat$DAS.F.stat
                } else {
                    DDD.stat <- trans_3D_stat$DAS.simes.stat
                }
                data2plot <- data.frame(
                    target = DDD.stat$target,
                    contrast = DDD.stat$contrast,
                    x = DDD.stat$maxdeltaPS,
                    y = -log10(DDD.stat$adj.pval)
                )
                data2plot$significance <- "Not significant"
                data2plot$significance[DDD.stat$adj.pval < pval_cut &
                    abs(DDD.stat$maxdeltaPS) >= deltaPS_cut] <- "Significant"
                q <- plotVolcano(
                    data2plot = data2plot,
                    xlab = "MaxdeltaPS of transcripts in each gene", ylab = "-log10(FDR)",
                    title = title.idx[i], col0 = col0, col1 = col1, size = size,
                    top.n = top.n
                )
            }

            if (i == "DE transcripts") {
                DDD.stat <- trans_3D_stat$DE.stat
                data2plot <- data.frame(
                    target = DDD.stat$target,
                    contrast = DDD.stat$contrast,
                    x = DDD.stat$log2FC,
                    y = -log10(DDD.stat$adj.pval)
                )
                data2plot$significance <- "Not significant"
                data2plot$significance[DDD.stat$adj.pval < pval_cut &
                    abs(DDD.stat$log2FC) >= l2fc_cut] <- "Significant"
                q <- plotVolcano(
                    data2plot = data2plot, xlab = "log2FC of transcripts",
                    ylab = "-log10(FDR)", title = title.idx[i],
                    col0 = col0, col1 = col1, size = size, top.n = top.n
                )
            }

            if (i == "DTU transcripts") {
                DDD.stat <- trans_3D_stat$DTU.stat
                data2plot <- data.frame(
                    target = DDD.stat$target,
                    contrast = DDD.stat$contrast,
                    x = DDD.stat$deltaPS,
                    y = -log10(DDD.stat$adj.pval)
                )
                data2plot$significance <- "Not significant"
                data2plot$significance[DDD.stat$adj.pval < pval_cut &
                    abs(DDD.stat$deltaPS) >= deltaPS_cut] <- "Significant"
                q <- plotVolcano(
                    data2plot = data2plot,
                    xlab = "deltaPS of transcripts", ylab = "-log10(FDR)",
                    title = title.idx[i],
                    col0 = col0, col1 = col1, size = size, top.n = top.n
                )
            }
            q
        })
        names(g) <- idx

        ######################################################################
        ## ----->> save plot
        lapply(names(g), function(i) {
            message(i)
            png(paste0(figure.folder, "/", i, " volcano plot.png"),
                width = 10, height = 6, units = "in",
                res = 150
            )
            print(g[[i]])
            dev.off()

            pdf(paste0(figure.folder, "/", i, " volcano plot.pdf"),
                width = 10, height = 6
            )
            print(g[[i]])
            dev.off()
        })

        ################################################################################
        ## ----->> DE vs DAS genes
        DE.genes <- unique(DE_genes$target)
        DAS.genes <- unique(DAS_genes$target)
        genes.flow.chart <- function() {
            plotFlowChart(
                expressed = target_high$genes_high,
                x = DE.genes,
                y = DAS.genes,
                type = "genes",
                pval.cutoff = pval_cut, lfc.cutoff = l2fc_cut,
                deltaPS.cutoff = deltaPS_cut
            )
        }
        genes.flow.chart()


        png(
            filename = paste0(figure.folder, "/Union set DE genes vs DAS genes.png"),
            width = 22 / 2.54, height = 13 / 2.54, units = "in", res = 300
        )
        genes.flow.chart()
        dev.off()

        pdf(
            file = paste0(figure.folder, "/Union set DE genes vs DAS genes.pdf"),
            width = 22 / 2.54, height = 13 / 2.54
        )
        genes.flow.chart()
        dev.off()

        ################################################################################
        ## ----->> DE vs DTU transcripts
        DE.trans <- unique(DE_trans$target)
        DTU.trans <- unique(DTU_trans$target)

        trans.flow.chart <- function() {
            plotFlowChart(
                expressed = target_high$trans_high,
                x = DE.trans,
                y = DTU.trans,
                type = "transcripts",
                pval.cutoff = pval_cut,
                lfc.cutoff = l2fc_cut,
                deltaPS.cutoff = deltaPS_cut
            )
        }

        trans.flow.chart()

        png(
            filename = paste0(figure.folder, "/Union set DE transcripts vs DTU transcripts.png"),
            width = 22 / 2.54, height = 13 / 2.54, units = "in", res = 300
        )
        trans.flow.chart()
        dev.off()

        pdf(
            file = paste0(figure.folder, "/Union set DE transcripts vs DTU transcripts.pdf"),
            width = 22 / 2.54, height = 13 / 2.54
        )
        trans.flow.chart()
        dev.off()


        contrast.idx <- contrast[1]
        ################################################################################
        ## ----->> DE vs DAS genes
        x <- unlist(DEvsDAS_results[DEvsDAS_results$Contrast == contrast.idx, -1])
        if (length(x) == 0) {
            message("No DE and/or DAS genes")
        } else {
            names(x) <- c("DE", "DE&DAS", "DAS")
            g <- plotEulerDiagram(x = x, fill = gg.color.hue(2))
            g
            grid.arrange(g, top = textGrob("DE vs DAS genes", gp = gpar(cex = 1.2)))
        }

        ################################################################################
        ## ----->> DE vs DTU transcripts
        x <- unlist(DEvsDTU_results[DEvsDTU_results$Contrast == contrast.idx, -1])
        if (length(x) == 0) {
            message("No DE and/or DTU transcripts")
        } else {
            names(x) <- c("DE", "DE&DTU", "DTU")
            g <- plotEulerDiagram(x = x, fill = gg.color.hue(2))
            g
            grid.arrange(g, top = textGrob("DE vs DTU transcripts", gp = gpar(cex = 1.2)))
        }

        show("==========> Step 5 Make plot")

        ################################################################################
        ## ----->> DE genes
        targets <- unique(DE_genes$target)
        data2heatmap <- txi_genes$abundance[targets, ]
        column_title <- paste0(length(targets), " DE genes")
        data2plot <- rowmean(
            x = t(data2heatmap),
            group = metatable$label,
            reorder = F
        )
        data2plot <- t(scale(data2plot))
        hc.dist <- dist(data2plot, method = dist_method)
        hc <- fastcluster::hclust(hc.dist, method = cluster_method)
        clusters <- cutree(hc, k = cluster_number)
        clusters <- reorderClusters(clusters = clusters, dat = data2plot)

        ### save the target list in each cluster to result folder
        x <- split(names(clusters), clusters)
        x <- lapply(names(x), function(i) {
            data.frame(Clusters = i, Targets = x[[i]])
        })
        x <- do.call(rbind, x)
        colnames(x) <- c("Clusters", "Targets")

        g <- Heatmap(as.matrix(data2plot),
            name = "Z-scores",
            cluster_rows = TRUE,
            clustering_method_rows = cluster_method,
            row_dend_reorder = T,
            show_row_names = FALSE,
            show_column_names = ifelse(ncol(data2plot) > 10, F, T),
            cluster_columns = FALSE,
            split = clusters,
            column_title = column_title
        )

        draw(g, column_title = "Conditions", column_title_side = "bottom")

        ### save to figure
        png(paste0(figure.folder, "/Heatmap DE genes.png"),
            width = pmax(10, 1 * length(unique(metatable$label))) / 2.54, height = 20 / 2.54,
            units = "in", res = 300
        )
        draw(g, column_title = "Conditions", column_title_side = "bottom")
        dev.off()
        pdf(paste0(figure.folder, "/Heatmap DE genes.pdf"),
            width = pmax(10, 1 * length(unique(metatable$label))) / 2.54, height = 20 / 2.54
        )
        draw(g, column_title = "Conditions", column_title_side = "bottom")
        dev.off()


        ################################################################################
        ## ----->> DAS genes
        targets <- unique(DAS_genes$target)
        data2heatmap <- txi_genes$abundance[targets, ]
        column_title <- paste0(length(targets), " DAS genes")
        data2plot <- rowmean(x = t(data2heatmap), group = metatable$label, reorder = F)
        data2plot <- t(scale(data2plot))
        hc.dist <- dist(data2plot, method = dist_method)
        hc <- fastcluster::hclust(hc.dist, method = cluster_method)
        clusters <- cutree(hc, k = cluster_number)
        clusters <- reorderClusters(clusters = clusters, dat = data2plot)


        ### save the target list in each cluster to result folder
        x <- split(names(clusters), clusters)
        x <- lapply(names(x), function(i) {
            data.frame(Clusters = i, Targets = x[[i]])
        })
        x <- do.call(rbind, x)
        colnames(x) <- c("Clusters", "Targets")
        write.csv(x,
            file = paste0(result.folder, "/Target in each cluster heatmap ", column_title, ".csv"),
            row.names = F
        )
        ###############################
        g <- Heatmap(as.matrix(data2plot),
            name = "Z-scores",
            cluster_rows = TRUE,
            clustering_method_rows = cluster_method,
            row_dend_reorder = T,
            show_row_names = FALSE,
            show_column_names = ifelse(ncol(data2plot) > 10, F, T),
            cluster_columns = FALSE,
            split = clusters,
            column_title = column_title
        )

        draw(g, column_title = "Conditions", column_title_side = "bottom")

        ### save to figure
        png(paste0(figure.folder, "/Heatmap DAS genes.png"),
            width = pmax(10, 1 * length(unique(metatable$label))) / 2.54, height = 20 / 2.54, units = "in", res = 300
        )
        draw(g, column_title = "Conditions", column_title_side = "bottom")
        dev.off()
        pdf(paste0(figure.folder, "/Heatmap DAS genes.pdf"),
            width = pmax(10, 1 * length(unique(metatable$label))) / 2.54, height = 20 / 2.54
        )
        draw(g, column_title = "Conditions", column_title_side = "bottom")
        dev.off()


        show("==========> Step 6 HEATMAP    OK")

        params_list <- list()
        params_list$condition_n <- length(unique((metatable_new$label)))
        params_list$brep_n <- length(unique(metatable[, brep_col]))
        # params_list$srep_n = length(unique(metatable[,srep_col]))
        params_list$samples_n <- nrow(metatable_new)
        params_list$has_srep <- has_srep
        params_list$quant_method <- quant_method
        params_list$tximport_method <- tximport_method
        params_list$cpm_cut <- cpm_cut
        params_list$cpm_samples_n <- cpm_samples_n
        params_list$norm_method <- norm_method
        params_list$has_batcheffect <- has_batcheffect
        params_list$RUVseq_method <- RUVseq_method
        params_list$contrast <- contrast
        params_list$DE_pipeline <- DE_pipeline
        params_list$pval_adj_method <- pval_adj_method
        params_list$pval_cut <- pval_cut
        params_list$l2fc_cut <- l2fc_cut
        params_list$deltaPS_cut <- deltaPS_cut
        params_list$DAS_pval_method <- DAS_pval_method

        ## heatmap
        params_list$dist_method <- dist_method
        params_list$cluster_method <- cluster_method
        params_list$cluster_number <- cluster_number



        DDD.data$conditions <- metatable$label
        DDD.data$params_list <- params_list
        save(DDD.data, file = paste0(data.folder, "/DDD.data.RData"))
    }
    show(" ... SALVANDO RESULTADOS ... ")


    #### save results
    idx <- c(
        "DE_genes", "DAS_genes", "DE_trans", "DTU_trans", "samples", "contrast",
        "DDD_numbers", "DEvsDAS_results", "DEvsDTU_results", "RNAseq_info"
    )
    idx.names <- gsub("_", " ", idx)
    idx.names <- gsub("trans", "transcripts", idx.names)
    idx.names[1:4] <- paste0("Significant ", idx.names[1:4], " list and statistics")

    idx <- c(idx, "scores", "scores_filtered")
    idx.names <- c(
        idx.names, "Raw isoform switch scores",
        "Significant isoform switch scores"
    )
    for (i in seq_along(idx)) {
        if (is.null(DDD.data[[idx[i]]])) {
            next
        }
        write.csv(x = DDD.data[[idx[i]]], file = paste0(DDD.data$result.folder, "/", idx.names[i], ".csv"), row.names = F)
    }
    ### save transcript-gene mapping
    write.csv(
        x = DDD.data$mapping,
        file = paste0(DDD.data$result.folder, "/Transcript and gene mapping.csv"),
        row.names = F, na = ""
    )

    ### save 3d list
    ## save all gene/transcript statistics
    write.csv(
        x = DDD.data$genes_3D_stat$DE.stat,
        file = paste0(DDD.data$result.folder, "/DE gene testing statistics.csv"),
        row.names = F, na = ""
    )

    write.csv(
        x = DDD.data$trans_3D_stat$DE.stat,
        file = paste0(
            DDD.data$result.folder,
            "/DE transcripts testing statistics.csv"
        ),
        row.names = F, na = ""
    )
    if (!is.null(DAS.stat)) {
        if (DDD.data$params_list$DAS_pval_method == "F-test") {
            write.csv(
                x = DDD.data$trans_3D_stat$DAS.F.stat,
                file = paste0(
                    DDD.data$result.folder,
                    "/DAS genes testing statistics.csv"
                ),
                row.names = F, na = ""
            )
        }
        if (DDD.data$params_list$DAS_pval_method == "Simes") {
            write.csv(
                x = DDD.data$trans_3D_stat$DAS.simes.stat,
                file = paste0(
                    DDD.data$result.folder,
                    "/DAS genes testing statistics.csv"
                ),
                row.names = F, na = ""
            )
        }
    }
    write.csv(
        x = DDD.data$trans_3D_stat$DTU.stat,
        file = paste0(
            DDD.data$result.folder,
            "/DTU transcripts testing statistics.csv"
        ),
        row.names = F, na = ""
    )
}
write("t3drnaseq executado.", file = file(paste0(results, "/status.txt"), "a"), append = T)
show("TERMINADO_COM_SUCESSO")
