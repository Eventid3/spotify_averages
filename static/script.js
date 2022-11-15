
function newChart(avgList, parameter){
  const labels = [
      '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979',
      '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989',
      '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999',
      '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
      '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
      '2020', '2021',
      ];

  const averages = avgList;
  const para = parameter;
  let yAxis = "";

  if (para == "Loudness"){
      yAxis = "dB"
  }
  else if (para == "Valence" || para == "Danceability" || para == "Speechiness" || para == "Acousticness"){
      yAxis = "%";
  }
  else if (para == "Duration"){
      yAxis = "Seconds"
  }

  const data = {
  labels: labels,
  datasets: [{
      label: para,
      backgroundColor: 'rgb(30, 215, 96)',
      borderColor: 'rgb(30, 215, 96)', 
      data: averages,
      }]
  };

  const config = {
  type: 'line',
  data: data,
  options: {
      scales: {
        y: {
          grid:{
            color: 'rgb(80,80,80)',
          },
          title: {
            display: true,
            text: yAxis
          }
        },
        x: {
          grid:{
            color: 'rgb(80,80,80)'
          }
        }
      }     
    }
  };

  const myChart = new Chart(
      document.getElementById('myChart'),
      config
      );
};


const win = window.addEventListener("resize", function(){
  let width = window.innerWidth;
  const nav = document.querySelector("nav")
  if (width < 760)
  {
    nav.style.left = "-200px"
  }
  else
  {
    nav.style.left = "0px"
  }
});


function toggleNav(){
  const nav = document.querySelector("nav");

  if (nav.style.left === "-200px"){
    nav.style.left = "0px";
  }
  else {
    nav.style.left = "-200px";
  }
};


