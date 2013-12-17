set datafile separator ","
set terminal png size 900,400
set title "Outdoor temperature"
set ylabel "Temperature"
set xlabel "Day time"
set xdata time
set timefmt "%s"
set format x "%H:%M\n%d/%m"
#set key left top
set grid

#plot 'temperature.txt' using ($1+3600):3 smooth csplines lw 2 lt 2 title 'Outdoor' with lines
plot 'temperature.txt' using ($1+3600):3 lw 2 lt 2 title 'Outdoor' with lines
