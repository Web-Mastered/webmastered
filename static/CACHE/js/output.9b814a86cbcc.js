var cpuChart=new Chart("cpuChart",{type:"bar",data:{labels:['CPU 1',],datasets:[{label:'CPU Utilisation / (%)',data:['0',],backgroundColor:['rgb(255, 99, 132)'],hoverOffset:4,}]},options:{scales:{y:{beginAtZero:true,max:100,min:0,}},}});var cpuLoadAvgChart=new Chart("cpuLoadAvgChart",{type:"bar",data:{labels:['1 Min','5 Mins','15 Mins'],datasets:[{label:'Average CPU Utilisation / (%)',data:['0','0','0',],backgroundColor:['rgb(255, 99, 132)'],hoverOffset:4,}]},options:{scales:{y:{beginAtZero:true,max:100,min:0,}},}});var ramChart=new Chart("ramChart",{type:"pie",data:{labels:['Used / (%)','Free / (%)',],datasets:[{label:'RAM Utilisation / (%)',data:[47.19779629238933,52.80220370761067],backgroundColor:['rgb(255, 99, 132)','rgb(75, 192, 192)'],hoverOffset:4}]},options:{}});;