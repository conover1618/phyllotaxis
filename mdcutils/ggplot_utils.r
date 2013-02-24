library(ggplot2)

# From: http://wiki.stdout.org/rcookbook/Graphs/Multiple%20graphs%20on%20one%20page%20(ggplot2)/
# Called as: multiplot(p1, p2, p3, p4, cols=2)

multiplot <- function(..., plotlist=NULL, cols) {
    require(grid)

    # Make a list from the ... arguments and plotlist
    plots <- c(list(...), plotlist)

    numPlots = length(plots)

    # Make the panel
    plotCols = cols                          # Number of columns of plots
    plotRows = ceiling(numPlots/plotCols)    # Number of rows needed, calculated from # of cols

    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(plotRows, plotCols)))
    vplayout <- function(x, y)
        viewport(layout.pos.row = x, layout.pos.col = y, height=10)

    # Make each plot, in the correct location
    for (i in 1:numPlots) {
        curRow = ceiling(i/plotCols)
        curCol = (i-1) %% plotCols + 1
        print(plots[[i]], vp = vplayout(curRow, curCol ))
    }

}



read_date_counts <- function(filename) {
	ts = read.table(filename, head=TRUE, sep='\t')
	colnames(ts) <- c('bin', 'date', 'count')
	ts$date <- as.Date(ts$date, format = "%m-%d-%Y")
	return(ts)
}

plot.timeseries <- function(dat, xstr="", ystr="") { 
	a <- aes_string(x=xstr, y=ystr)
	m <- ggplot(dat, a) 
	m <- m + geom_line(aes=a)
	m
}



# Reads a file formatted as: id [tab] tab-separated values \n .. 
# Returns list of ids and values in one-to-one association
read.jagged_file <- function(filepath) { 
	con <- file(filepath) 
	open(con);
	ids <- list();
	vals <- list();
	current.line <- 1
	while (length(line <- readLines(con, n = 1, warn = FALSE)) > 0) {
		line_str <- unlist(strsplit(line, split=" "))
		id <- line_str[1]
		val <- line_str[2:length(line_str)]
	
		ids[[current.line]] <- id
		vals[[current.line]] <- val
		current.line <- current.line + 1
	}
	close(con)
	return( list(ids = ids, vals = vals) )
}

# Plot a timeseries using spikes
# qplot(data=q, x=bin, y=count, geom="segment", yend = 0, xend=bin, size=I(.5))


log.breaks <- function(mn, mx, base, numbins) {
	lmn = log(mn, base)
	lmx = log(mx, base)
	q = sprintf("Min: %s, Max: %s", lmn, lmx)
	
	breaks <- rep(0, numbins)
	
	idx = 1
	for(exp in seq(lmn, lmx, (lmx - lmn) / numbins)) {
		breaks[idx] = base^exp
		idx = idx + 1
		sprintf("%s:%s", idx, exp)
	}
	return(breaks)
}



# Plots one or more pdf's on the same coordinates using log/log scale and logarithmic binning
# x_list: 	list of sets of values to plot
# grpids:	id's in one-to-one correspondence with x_list

plot.hist_loglog <- function(x_list, grpids=c(''), base=10, numbins=50, xlab='', title='', filename='', facet=FALSE, width=7, height=5) { 
	
	multiple = TRUE
	if(typeof(x_list) != 'list'){
		x_list <- list(x_list)
		multiple = FALSE
	}
	
	gmx <- -Inf
	gmn <- Inf	
	for(i in 1:length(x_list)) {
		x <- x_list[[i]]
		if(min(x) < gmn) { gmn = min(x) }
		if(max(x) > gmx) { gmx = max(x) }
	}
	
	mids = c()
	density = c()
	grp = c()
	
	breaks <- log.breaks(gmn, gmx, base, numbins)
	for(i in 1:length(x_list)) {

		x <- x_list[[i]]
		h <- hist(x, breaks=breaks, plot=FALSE)
		
		mids <- c(mids, h$mids)
		density <- c(density, h$density)
		grp <- c(grp, rep(grpids[i], length(h$mids)))
	}
	
	df <- data.frame(grp=grp, mids=mids, density=density)
	
	p <- ggplot(data= df, aes(x=mids, y=density))	
	if(multiple) {
		if(!facet) {
			p <- p + geom_point(size=1.4,  aes(color=factor(grp)))
		}
		if(facet) {
			p <- p + geom_point(size=1.4) + facet_grid(grp ~ .)
		}
	}
	else {
		p <- p + geom_point(size=1.4)
	}
	p <- p + scale_x_log10(xlab) + scale_y_log10('Density') + opts(title=title)
	
	if(filename == '') {
		print(p)
	}
	else{
		ggsave(plot=p, filename=filename, width=width, height=height)
		sprintf("Wrote to: %s", filename)
		#dev.off()
	}
}

# Plot a column from a file using plot.hist_loglog
# plot.hist_loglog_fromfile <- function(filename, colidx, grpids=c(''), omit_zeros=FALSE, header=FALSE, comment.char = '!', base=10, numbins=50, xlab='', title='', outfile='', width=5, height=5) {
# 	dat <- read.table(filename, header=header, comment.char= comment.char)
# 	x_list <- dat[,colidx]
# 	
# 	if(omit_zeros)		x_list = x_list[x_list > 0]	
# 	}
# 	plot.hist_loglog(x_list, grpids=grpids, base=base, numbins=numbins, xlab=xlab, title=title, filename=outfile, width=width, height=height)
# }
