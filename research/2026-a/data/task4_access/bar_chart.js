function trunc_val(valore){

    if (valore<= 30){
        return valore;

    }else{
        return 30;
    }
}






 

 

function chart_test(data){


    ////////////////////////////////////////////////////////////// 
    ////////////////////////// Data ////////////////////////////// 
    ////////////////////////////////////////////////////////////// 
    //console.log(data)
    var data_bike = [ trunc_val(data.b_b),trunc_val(data.c_b),trunc_val(data.d_b),trunc_val(data.e_b),trunc_val(data.f_b),trunc_val(data.g_b),trunc_val(data.h_b),trunc_val(data.i_b),trunc_val(data.l_b)]
       
    var data_foot = [ trunc_val(data.b_f),trunc_val(data.c_f),trunc_val(data.d_f),trunc_val(data.e_f),trunc_val(data.f_f),trunc_val(data.g_f),trunc_val(data.h_f),trunc_val(data.i_f),trunc_val(data.l_f)]
       
    const  ctx = document.getElementById('barChart');

    let chartStatus = Chart.getChart(ctx); // <canvas> id
    if (chartStatus != undefined) {
      chartStatus.destroy();
    }
 
   
            
   
   barChart(ctx, data_bike,data_foot);
    }
    
    
    
    
    /////////////////////////////////////////////////////////
    /////////////// The Radar Chart Function ////////////////
    /////////////// Written by Nadieh Bremer ////////////////
    ////////////////// VisualCinnamon.com ///////////////////
    /////////// Inspired by the code of alangrafu ///////////
    /////////////////////////////////////////////////////////
        
    function barChart( ctx,data_bike,data_foot) {
      
        new Chart(ctx, {
            type: 'bar',
   
            data: {
              labels: [  "Outdoor activities","Learning","Supplies","Eating","Moving","Cultural activities","Physical exercise","Services","Healthcare"],
              datasets: [{
                label: 'Bike',
                data: data_bike,
                borderWidth: 1,
                borderColor: '#EDC951',
                backgroundColor: "#EDC951",
              },{
                label: 'Foot',
                data: data_foot,
                borderWidth: 1,
                borderColor: "#00A0B0",
                backgroundColor: '#00A0B0',
              }]
            },
            options: {
              scales: {
         
                y: {
                  beginAtZero: true,
                  stepValue: 5,
                        max: 30,
                        grid: {
                            color: (c) => {if(c['tick']['value'] == 15) return 'red'; else return 'grey';}, // this here
                          },
                          ticks: {
                            color: (c) => {if(c['tick']['value'] == 15) return 'red'; else return 'grey';}, // this here
                          },
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
              }
            }
          });
        
    }//RadarChart



    function chart_test1(data){


      ////////////////////////////////////////////////////////////// 
      ////////////////////////// Data ////////////////////////////// 
      ////////////////////////////////////////////////////////////// 
      //console.log(data)
      var data_bike = [ trunc_val(data.b_b),trunc_val(data.c_b),trunc_val(data.d_b),trunc_val(data.e_b),trunc_val(data.f_b),trunc_val(data.g_b),trunc_val(data.h_b),trunc_val(data.i_b),trunc_val(data.l_b)]
         
      var data_foot = [ trunc_val(data.b_f),trunc_val(data.c_f),trunc_val(data.d_f),trunc_val(data.e_f),trunc_val(data.f_f),trunc_val(data.g_f),trunc_val(data.h_f),trunc_val(data.i_f),trunc_val(data.l_f)]
         
      const  ctx = document.getElementById('radarchart');
  
      let chartStatus = Chart.getChart(ctx); // <canvas> id
      if (chartStatus != undefined) {
        chartStatus.destroy();
      }
   
     
              
     
     barCharto(ctx, data_bike,data_foot);
      }
      
      
      
      
  
      function barCharto( ctx,data_bike,data_foot) {
        
          new Chart(ctx, {

            type: 'bar',
            data:   {
              labels: [  "Outdoor activities","Learning","Supplies","Eating","Moving","Cultural activities","Physical exercise","Services","Healthcare"],
              datasets: [{
                label: 'Bike',
                data: data_bike,
                borderWidth: 1,
                borderColor: '#EDC951',
                backgroundColor: "#EDC951",
              },{
                label: 'Foot',
                data: data_foot,
                borderWidth: 1,
                borderColor: "#00A0B0",
                backgroundColor: '#00A0B0',
              }
              ]
            },
            options: {
              responsive: true,
              indexAxis: 'y',
              x: {
               
                beginAtZero: true,
                step: 15,
                      max: 30,
                      grid: {
                          color: (c) => {if(c['tick']['value'] == 15) return 'red'; else return 'grey';}, // this here
                        },
                        ticks: {
                          color: (c) => {if(c['tick']['value'] == 15) return 'red'; else return 'grey';}, // this here
                        },
                    
              },
              y:{
              
                    ticks: {
                      font: {
                        size: 10,
                        stepSize: 1,
                      }
                    }
                
            
            }
          }
 
 
            

            });
          
      }//RadarChart
  