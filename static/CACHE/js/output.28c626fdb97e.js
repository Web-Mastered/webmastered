var cpuChart=new Chart("cpuChart",{type:"bar",data:{labels:['CPU 1',],datasets:[{label:'CPU Utilisation / (%)',data:['0',],backgroundColor:['rgb(255, 99, 132)'],hoverOffset:4,}]},options:{scales:{y:{beginAtZero:true,max:100,min:0,}},}});var cpuLoadAvgChart=new Chart("cpuLoadAvgChart",{type:"bar",data:{labels:['1 Min','5 Mins','15 Mins'],datasets:[{label:'Average CPU Utilisation / (%)',data:['0','0','0',],backgroundColor:['rgb(255, 99, 132)'],hoverOffset:4,}]},options:{scales:{y:{beginAtZero:true,max:100,min:0,}},}});var ramChart=new Chart("ramChart",{type:"pie",data:{labels:['Used / (%)','Free / (%)',],datasets:[{label:'RAM Utilisation / (%)',data:[49.245461023115844,50.754538976884156],backgroundColor:['rgb(255, 99, 132)','rgb(75, 192, 192)'],hoverOffset:4}]},options:{}});var diskChart=new Chart("diskChart",{type:"pie",data:{labels:['Used / (%)','Free / (%)',],datasets:[{label:'RAM Utilisation / (%)',data:[16.181624737978733,83.81837526202126],backgroundColor:['rgb(255, 99, 132)','rgb(75, 192, 192)'],hoverOffset:4}]},options:{}});;