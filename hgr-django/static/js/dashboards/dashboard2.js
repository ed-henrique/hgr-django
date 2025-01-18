document.addEventListener("DOMContentLoaded", function() {
  ("use strict");

  const numberLiteralFormatter = new Intl.NumberFormat("en", {
    style: "decimal",
    useGrouping: false,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  const numberFormatter = new Intl.NumberFormat("pt-BR", {
    style: "decimal",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  const percentFormatter = new Intl.NumberFormat("pt-BR", {
    style: "percent",
    minimumIntegerDigits: 2,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  const dadosEntradasPorDiaPorSetor = {};
  const dadosEntradasPorDia = JSON.parse(document.getElementById('dados-entradas-por-dia').textContent);
  let tamanhoMaximoDadosEntradasPorDiaPorSetor = dadosEntradasPorDia.length;
  dadosEntradasPorDia.forEach((el, i) => {
    el["EntradasPorDiaPorSetor"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetorDeDestino"];
      const nome = eli["NomeSetorDeDestino"];
      let itemSetor = dadosEntradasPorDiaPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosEntradasPorDiaPorSetor[eli["NomeSetorDeDestino"]] = itemSetor;
    });
  });
  Object.keys(dadosEntradasPorDiaPorSetor).forEach((el) => {
    if (dadosEntradasPorDiaPorSetor[el].data.length < tamanhoMaximoDadosEntradasPorDiaPorSetor) {
      for (let i = dadosEntradasPorDiaPorSetor[el].data.length; i < tamanhoMaximoDadosEntradasPorDiaPorSetor; i++) {
        dadosEntradasPorDiaPorSetor[el].data.push(null);
      }
    }
  });
  var entradasPorDiaOpcoes = {
    series: Object.values(dadosEntradasPorDiaPorSetor),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosEntradasPorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosCirurgiasPorDiaPorSetor = {};
  const dadosCirurgiasPorDia = JSON.parse(document.getElementById('dados-cirurgias-por-dia').textContent);
  let tamanhoMaximoDadosCirurgiasPorDiaPorSetor = dadosCirurgiasPorDia.length;
  dadosCirurgiasPorDia.forEach((el, i) => {
    el["CirurgiasPorDiaPorSetor"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetor"];
      const nome = eli["NomeSetor"];
      let itemSetor = dadosCirurgiasPorDiaPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosCirurgiasPorDiaPorSetor[eli["NomeSetor"]] = itemSetor;
    });
  });
  Object.keys(dadosCirurgiasPorDiaPorSetor).forEach((el) => {
    if (dadosCirurgiasPorDiaPorSetor[el].data.length < tamanhoMaximoDadosCirurgiasPorDiaPorSetor) {
      for (let i = dadosCirurgiasPorDiaPorSetor[el].data.length; i < tamanhoMaximoDadosCirurgiasPorDiaPorSetor; i++) {
        dadosCirurgiasPorDiaPorSetor[el].data.push(null);
      }
    }
  });
  var cirurgiasPorDiaOpcoes = {
    series: Object.values(dadosCirurgiasPorDiaPorSetor),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosCirurgiasPorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosCirurgiasBemSucedidasPorDiaPorSetor = {};
  const dadosCirurgiasBemSucedidasPorDia = JSON.parse(document.getElementById('dados-taxa-efetividade-cirurgica').textContent);
  let tamanhoMaximoDadosCirurgiasBemSucedidasPorDiaPorSetor = dadosCirurgiasBemSucedidasPorDia.length;
  dadosCirurgiasBemSucedidasPorDia.forEach((el, i) => {
    el["CirurgiasBemSucedidasPorDiaPorSetor"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetor"];
      const nome = eli["NomeSetor"];
      let itemSetor = dadosCirurgiasBemSucedidasPorDiaPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosCirurgiasBemSucedidasPorDiaPorSetor[eli["NomeSetor"]] = itemSetor;
    });
  });
  Object.keys(dadosCirurgiasBemSucedidasPorDiaPorSetor).forEach((el) => {
    if (dadosCirurgiasBemSucedidasPorDiaPorSetor[el].data.length < tamanhoMaximoDadosCirurgiasBemSucedidasPorDiaPorSetor) {
      for (let i = dadosCirurgiasBemSucedidasPorDiaPorSetor[el].data.length; i < tamanhoMaximoDadosCirurgiasBemSucedidasPorDiaPorSetor; i++) {
        dadosCirurgiasBemSucedidasPorDiaPorSetor[el].data.push(null);
      }
    }
  });
  var cirurgiasBemSucedidasPorDiaOpcoes = {
    series: [{
      name: 'HGR',
      data: Array.from({ length: dadosCirurgiasPorDia.length }, (_, i) => {
        const iCirurgiasBemSucedidas = Object.values(dadosCirurgiasBemSucedidasPorDiaPorSetor).reduce((acc, cur) => {
          return acc + (cur.data[i] === null ? 0 : cur.data[i]);
        }, 0);

        const iCirurgiasDia = Object.values(dadosCirurgiasPorDiaPorSetor).reduce((acc, cur) => {
          return acc + (cur.data[i] === null ? 0 : cur.data[i]);
        }, 0);

        return iCirurgiasBemSucedidas / (iCirurgiasDia === 0 ? 1 : iCirurgiasDia);
      }),
    }],
    chart: {
      height: 350,
      type: 'line',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: true,
      enabledOnSeries: [0],
      formatter: (val) => {
        return percentFormatter.format(val);
      }
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosCirurgiasPorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: (val) => {
          return percentFormatter.format(val);
        }
      },
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosEntradasPreCirurgicasPorDiaPorSetor = {};
  const dadosEntradasPreCirurgicasPorDia = JSON.parse(document.getElementById('dados-entradas-pre-cirurgicas-por-dia').textContent);
  let tamanhoMaximoDadosEntradasPreCirurgicasPorDiaPorSetor = dadosEntradasPreCirurgicasPorDia.length;
  dadosEntradasPreCirurgicasPorDia.forEach((el, i) => {
    el["EntradasPreCirurgicasPorDiaPorSetor"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetorDeDestino"];
      const nome = eli["NomeSetorDeDestino"];
      let itemSetor = dadosEntradasPreCirurgicasPorDiaPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosEntradasPreCirurgicasPorDiaPorSetor[eli["NomeSetorDeDestino"]] = itemSetor;
    });
  });
  Object.keys(dadosEntradasPreCirurgicasPorDiaPorSetor).forEach((el) => {
    if (dadosEntradasPreCirurgicasPorDiaPorSetor[el].data.length < tamanhoMaximoDadosEntradasPreCirurgicasPorDiaPorSetor) {
      for (let i = dadosEntradasPreCirurgicasPorDiaPorSetor[el].data.length; i < tamanhoMaximoDadosEntradasPreCirurgicasPorDiaPorSetor; i++) {
        dadosEntradasPreCirurgicasPorDiaPorSetor[el].data.push(null);
      }
    }
  });
  var entradasPreCirurgicasPorDiaOpcoes = {
    series: Object.values(dadosEntradasPreCirurgicasPorDiaPorSetor),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosEntradasPreCirurgicasPorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosSaidasPorDiaPorSetor = {};
  const dadosSaidasPorDia = JSON.parse(document.getElementById('dados-saidas-por-dia-por-setor').textContent);
  let tamanhoMaximoDadosSaidasPorDiaPorSetor = dadosSaidasPorDia.length;
  dadosSaidasPorDia.forEach((el, i) => {
    el["SaidasPorDia"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetorDeOrigem"];
      const nome = eli["NomeSetorDeOrigem"];
      let itemSetor = dadosSaidasPorDiaPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosSaidasPorDiaPorSetor[eli["NomeSetorDeOrigem"]] = itemSetor;
    });
  });
  Object.keys(dadosSaidasPorDiaPorSetor).forEach((el) => {
    if (dadosSaidasPorDiaPorSetor[el].data.length < tamanhoMaximoDadosSaidasPorDiaPorSetor) {
      for (let i = dadosSaidasPorDiaPorSetor[el].data.length; i < tamanhoMaximoDadosSaidasPorDiaPorSetor; i++) {
        dadosSaidasPorDiaPorSetor[el].data.push(null);
      }
    }
  });
  var saidasPorDiaPorSetorOpcoes = {
    series: Object.values(dadosSaidasPorDiaPorSetor),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosSaidasPorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosSaidasPorDiaPorTipoDeSaida = {};
  const dadosSaidasPorDia2 = JSON.parse(document.getElementById('dados-saidas-por-dia-por-tipo-de-saida').textContent);
  let tamanhoMaximoDadosSaidasPorDiaPorTipoDeSaida = dadosSaidasPorDia2.length;
  dadosSaidasPorDia2.forEach((el, i) => {
    el["SaidasPorDia"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorTipoDeSaida"];
      const nome = eli["NomeTipoDeSaida"];
      let itemSetor = dadosSaidasPorDiaPorTipoDeSaida[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosSaidasPorDiaPorTipoDeSaida[eli["NomeTipoDeSaida"]] = itemSetor;
    });
  });
  Object.keys(dadosSaidasPorDiaPorTipoDeSaida).forEach((el) => {
    if (dadosSaidasPorDiaPorTipoDeSaida[el].data.length < tamanhoMaximoDadosSaidasPorDiaPorTipoDeSaida) {
      for (let i = dadosSaidasPorDiaPorTipoDeSaida[el].data.length; i < tamanhoMaximoDadosSaidasPorDiaPorTipoDeSaida; i++) {
        dadosSaidasPorDiaPorTipoDeSaida[el].data.push(null);
      }
    }
  });
  var saidasPorDiaPorTipoDeSaidaOpcoes = {
    series: Object.values(dadosSaidasPorDiaPorTipoDeSaida),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosSaidasPorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosSaidasAntes24PorDiaPorSetor = {};
  const dadosSaidasAntes24PorDia = JSON.parse(document.getElementById('dados-saidas-antes-24-por-dia-por-setor').textContent);
  let tamanhoMaximoDadosSaidasAntes24PorDiaPorSetor = dadosSaidasAntes24PorDia.length;
  dadosSaidasAntes24PorDia.forEach((el, i) => {
    el["SaidasPorDia"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetorDeOrigem"];
      const nome = eli["NomeSetorDeOrigem"];
      let itemSetor = dadosSaidasAntes24PorDiaPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosSaidasAntes24PorDiaPorSetor[eli["NomeSetorDeOrigem"]] = itemSetor;
    });
  });
  Object.keys(dadosSaidasAntes24PorDiaPorSetor).forEach((el) => {
    if (dadosSaidasAntes24PorDiaPorSetor[el].data.length < tamanhoMaximoDadosSaidasAntes24PorDiaPorSetor) {
      for (let i = dadosSaidasAntes24PorDiaPorSetor[el].data.length; i < tamanhoMaximoDadosSaidasAntes24PorDiaPorSetor; i++) {
        dadosSaidasAntes24PorDiaPorSetor[el].data.push(null);
      }
    }
  });
  var saidasAntes24PorDiaPorSetorOpcoes = {
    series: Object.values(dadosSaidasAntes24PorDiaPorSetor),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosSaidasAntes24PorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosSaidasAntes24PorDiaPorTipoDeSaida = {};
  const dadosSaidasAntes24PorDia2 = JSON.parse(document.getElementById('dados-saidas-antes-24-por-dia-por-tipo-de-saida').textContent);
  let tamanhoMaximoDadosSaidasAntes24PorDiaPorTipoDeSaida = dadosSaidasAntes24PorDia2.length;
  dadosSaidasAntes24PorDia2.forEach((el, i) => {
    el["SaidasPorDia"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorTipoDeSaida"];
      const nome = eli["NomeTipoDeSaida"];
      let itemSetor = dadosSaidasAntes24PorDiaPorTipoDeSaida[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosSaidasAntes24PorDiaPorTipoDeSaida[eli["NomeTipoDeSaida"]] = itemSetor;
    });
  });
  Object.keys(dadosSaidasAntes24PorDiaPorTipoDeSaida).forEach((el) => {
    if (dadosSaidasAntes24PorDiaPorTipoDeSaida[el].data.length < tamanhoMaximoDadosSaidasAntes24PorDiaPorTipoDeSaida) {
      for (let i = dadosSaidasAntes24PorDiaPorTipoDeSaida[el].data.length; i < tamanhoMaximoDadosSaidasAntes24PorDiaPorTipoDeSaida; i++) {
        dadosSaidasAntes24PorDiaPorTipoDeSaida[el].data.push(null);
      }
    }
  });
  var saidasAntes24PorDiaPorTipoDeSaidaOpcoes = {
    series: Object.values(dadosSaidasAntes24PorDiaPorTipoDeSaida),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosSaidasAntes24PorDia2.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosSaidasDepois24PorDiaPorSetor = {};
  const dadosSaidasDepois24PorDia = JSON.parse(document.getElementById('dados-saidas-depois-24-por-dia-por-setor').textContent);
  let tamanhoMaximoDadosSaidasDepois24PorDiaPorSetor = dadosSaidasDepois24PorDia.length;
  dadosSaidasDepois24PorDia.forEach((el, i) => {
    el["SaidasPorDia"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetorDeOrigem"];
      const nome = eli["NomeSetorDeOrigem"];
      let itemSetor = dadosSaidasDepois24PorDiaPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosSaidasDepois24PorDiaPorSetor[eli["NomeSetorDeOrigem"]] = itemSetor;
    });
  });
  Object.keys(dadosSaidasDepois24PorDiaPorSetor).forEach((el) => {
    if (dadosSaidasDepois24PorDiaPorSetor[el].data.length < tamanhoMaximoDadosSaidasDepois24PorDiaPorSetor) {
      for (let i = dadosSaidasDepois24PorDiaPorSetor[el].data.length; i < tamanhoMaximoDadosSaidasDepois24PorDiaPorSetor; i++) {
        dadosSaidasDepois24PorDiaPorSetor[el].data.push(null);
      }
    }
  });
  var saidasDepois24PorDiaPorSetorOpcoes = {
    series: Object.values(dadosSaidasDepois24PorDiaPorSetor),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosSaidasDepois24PorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosSaidasDepois24PorDiaPorTipoDeSaida = {};
  const dadosSaidasDepois24PorDia2 = JSON.parse(document.getElementById('dados-saidas-depois-24-por-dia-por-tipo-de-saida').textContent);
  let tamanhoMaximoDadosSaidasDepois24PorDiaPorTipoDeSaida = dadosSaidasDepois24PorDia2.length;
  dadosSaidasDepois24PorDia2.forEach((el, i) => {
    el["SaidasPorDia"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorTipoDeSaida"];
      const nome = eli["NomeTipoDeSaida"];
      let itemSetor = dadosSaidasDepois24PorDiaPorTipoDeSaida[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosSaidasDepois24PorDiaPorTipoDeSaida[eli["NomeTipoDeSaida"]] = itemSetor;
    });
  });
  Object.keys(dadosSaidasDepois24PorDiaPorTipoDeSaida).forEach((el) => {
    if (dadosSaidasDepois24PorDiaPorTipoDeSaida[el].data.length < tamanhoMaximoDadosSaidasDepois24PorDiaPorTipoDeSaida) {
      for (let i = dadosSaidasDepois24PorDiaPorTipoDeSaida[el].data.length; i < tamanhoMaximoDadosSaidasDepois24PorDiaPorTipoDeSaida; i++) {
        dadosSaidasDepois24PorDiaPorTipoDeSaida[el].data.push(null);
      }
    }
  });
  var saidasDepois24PorDiaPorTipoDeSaidaOpcoes = {
    series: Object.values(dadosSaidasDepois24PorDiaPorTipoDeSaida),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosSaidasDepois24PorDia2.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosSaidasPosCirurgicasPorDiaPorSetor = {};
  const dadosSaidasPosCirurgicasPorDia = JSON.parse(document.getElementById('dados-saidas-pos-cirurgicas-por-dia-por-setor').textContent);
  let tamanhoMaximoDadosSaidasPosCirurgicasPorDiaPorSetor = dadosSaidasPosCirurgicasPorDia.length;
  dadosSaidasPosCirurgicasPorDia.forEach((el, i) => {
    el["SaidasPosCirurgicasPorDia"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetorDeOrigem"];
      const nome = eli["NomeSetorDeOrigem"];
      let itemSetor = dadosSaidasPosCirurgicasPorDiaPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosSaidasPosCirurgicasPorDiaPorSetor[eli["NomeSetorDeOrigem"]] = itemSetor;
    });
  });
  Object.keys(dadosSaidasPosCirurgicasPorDiaPorSetor).forEach((el) => {
    if (dadosSaidasPosCirurgicasPorDiaPorSetor[el].data.length < tamanhoMaximoDadosSaidasPosCirurgicasPorDiaPorSetor) {
      for (let i = dadosSaidasPosCirurgicasPorDiaPorSetor[el].data.length; i < tamanhoMaximoDadosSaidasPosCirurgicasPorDiaPorSetor; i++) {
        dadosSaidasPosCirurgicasPorDiaPorSetor[el].data.push(null);
      }
    }
  });
  var saidasPosCirurgicasPorDiaPorSetorOpcoes = {
    series: Object.values(dadosSaidasPosCirurgicasPorDiaPorSetor),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosSaidasPosCirurgicasPorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosSaidasPosCirurgicasPorDiaPorTipoDeSaida = {};
  const dadosSaidasPosCirurgicasPorDia2 = JSON.parse(document.getElementById('dados-saidas-pos-cirurgicas-por-dia-por-tipo-de-saida').textContent);
  let tamanhoMaximoDadosSaidasPosCirurgicasPorDiaPorTipoDeSaida = dadosSaidasPosCirurgicasPorDia2.length;
  dadosSaidasPosCirurgicasPorDia2.forEach((el, i) => {
    el["SaidasPosCirurgicasPorDia"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorTipoDeSaida"];
      const nome = eli["NomeTipoDeSaida"];
      let itemSetor = dadosSaidasPosCirurgicasPorDiaPorTipoDeSaida[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosSaidasPosCirurgicasPorDiaPorTipoDeSaida[eli["NomeTipoDeSaida"]] = itemSetor;
    });
  });
  Object.keys(dadosSaidasPosCirurgicasPorDiaPorTipoDeSaida).forEach((el) => {
    if (dadosSaidasPosCirurgicasPorDiaPorTipoDeSaida[el].data.length < tamanhoMaximoDadosSaidasPosCirurgicasPorDiaPorTipoDeSaida) {
      for (let i = dadosSaidasPosCirurgicasPorDiaPorTipoDeSaida[el].data.length; i < tamanhoMaximoDadosSaidasPosCirurgicasPorDiaPorTipoDeSaida; i++) {
        dadosSaidasPosCirurgicasPorDiaPorTipoDeSaida[el].data.push(null);
      }
    }
  });
  var saidasPosCirurgicasPorDiaPorTipoDeSaidaOpcoes = {
    series: Object.values(dadosSaidasPosCirurgicasPorDiaPorTipoDeSaida),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosSaidasPosCirurgicasPorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosPacientesDiaPorSetor = {};
  const dadosPacientesDia = JSON.parse(document.getElementById('dados-pacientes-dia').textContent);
  let tamanhoMaximoDadosPacientesDiaPorSetor = dadosPacientesDia.length;
  dadosPacientesDia.forEach((el, i) => {
    el["PacientesPorDiaPorSetor"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetor"];
      const nome = eli["NomeSetor"];
      let itemSetor = dadosPacientesDiaPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosPacientesDiaPorSetor[eli["NomeSetor"]] = itemSetor;
    });
  });
  Object.keys(dadosPacientesDiaPorSetor).forEach((el) => {
    if (dadosPacientesDiaPorSetor[el].data.length < tamanhoMaximoDadosPacientesDiaPorSetor) {
      for (let i = dadosPacientesDiaPorSetor[el].data.length; i < tamanhoMaximoDadosPacientesDiaPorSetor; i++) {
        dadosPacientesDiaPorSetor[el].data.push(null);
      }
    }
  });
  var pacientesDiaOpcoes = {
    series: Object.values(dadosPacientesDiaPorSetor),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosPacientesDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosLeitosDiaPorSetor = {};
  const dadosLeitosDia = JSON.parse(document.getElementById('dados-leitos-dia').textContent);
  let tamanhoMaximoDadosLeitosDiaPorSetor = dadosLeitosDia.length;
  dadosLeitosDia.forEach((el, i) => {
    el["LeitosPorDiaPorSetor"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetor"];
      const nome = eli["NomeSetor"];
      let itemSetor = dadosLeitosDiaPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosLeitosDiaPorSetor[eli["NomeSetor"]] = itemSetor;
    });
  });
  Object.keys(dadosLeitosDiaPorSetor).forEach((el) => {
    if (dadosLeitosDiaPorSetor[el].data.length < tamanhoMaximoDadosLeitosDiaPorSetor) {
      for (let i = dadosLeitosDiaPorSetor[el].data.length; i < tamanhoMaximoDadosLeitosDiaPorSetor; i++) {
        dadosLeitosDiaPorSetor[el].data.push(null);
      }
    }
  });
  var leitosDiaOpcoes = {
    series: Object.values(dadosLeitosDiaPorSetor),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosLeitosDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosTransferenciasEnviadasPorSetor = {};
  const dadosTransferenciasEnviadas = JSON.parse(document.getElementById('dados-transferencias-enviadas').textContent);
  let tamanhoMaximoDadosTransferenciasEnviadasPorSetor = dadosTransferenciasEnviadas.length;
  dadosTransferenciasEnviadas.forEach((el, i) => {
    el["TransferenciasEnviadasPorDiaPorSetor"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetorDeOrigem"];
      const nome = eli["NomeSetorDeOrigem"];
      let itemSetor = dadosTransferenciasEnviadasPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosTransferenciasEnviadasPorSetor[eli["NomeSetorDeOrigem"]] = itemSetor;
    });
  });
  Object.keys(dadosTransferenciasEnviadasPorSetor).forEach((el) => {
    if (dadosTransferenciasEnviadasPorSetor[el].data.length < tamanhoMaximoDadosTransferenciasEnviadasPorSetor) {
      for (let i = dadosTransferenciasEnviadasPorSetor[el].data.length; i < tamanhoMaximoDadosTransferenciasEnviadasPorSetor; i++) {
        dadosTransferenciasEnviadasPorSetor[el].data.push(null);
      }
    }
  });
  var transferenciasEnviadasPorSetorOpcoes = {
    series: Object.values(dadosTransferenciasEnviadasPorSetor),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosTransferenciasEnviadas.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  const dadosTransferenciasRecebidasPorSetor = {};
  const dadosTransferenciasRecebidas = JSON.parse(document.getElementById('dados-transferencias-recebidas').textContent);
  let tamanhoMaximoDadosTransferenciasRecebidasPorSetor = dadosTransferenciasRecebidas.length;
  dadosTransferenciasRecebidas.forEach((el, i) => {
    el["TransferenciasRecebidasPorDiaPorSetor"].forEach((eli) => {
      const quantidade = eli["Quantidade"];
      const cor = eli["CorSetorDeDestino"];
      const nome = eli["NomeSetorDeDestino"];
      let itemSetor = dadosTransferenciasRecebidasPorSetor[nome];

      if (itemSetor !== undefined) {
        if (itemSetor.data.length === i) {
          itemSetor.data.push(quantidade)
        } else if (itemSetor.data.length < i) {
          for (let j = itemSetor.data.length; j < i; j++) {
            itemSetor.data.push(null);
          }
          itemSetor.data.push(quantidade)
        }
      } else {
        itemSetor = {};
        itemSetor.data = Array(i).fill(null);
        itemSetor.data.push(quantidade);
        itemSetor.color = cor;
        itemSetor.name = nome;
      }

      dadosTransferenciasRecebidasPorSetor[eli["NomeSetorDeDestino"]] = itemSetor;
    });
  });
  Object.keys(dadosTransferenciasRecebidasPorSetor).forEach((el) => {
    if (dadosTransferenciasRecebidasPorSetor[el].data.length < tamanhoMaximoDadosTransferenciasRecebidasPorSetor) {
      for (let i = dadosTransferenciasRecebidasPorSetor[el].data.length; i < tamanhoMaximoDadosTransferenciasRecebidasPorSetor; i++) {
        dadosTransferenciasRecebidasPorSetor[el].data.push(null);
      }
    }
  });
  var transferenciasRecebidasPorSetorOpcoes = {
    series: Object.values(dadosTransferenciasRecebidasPorSetor),
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosTransferenciasRecebidas.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value, { series, dataPointIndex }) {
          let total = series.map((el) => el[dataPointIndex]).reduce((acc, cur) => {
            if (cur !== null) {
              return acc + cur;
            }

            return acc;
          }, 0);
          total = total === 0 ? 1 : total;

          if (isNaN(value)) {
            return `${numberFormatter.format(0)} (${percentFormatter.format(0)})`;
          }

          return `${numberFormatter.format(value === null ? 0 : value)} (${percentFormatter.format(value / total)})`;
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  var taxaDeOcupacaoHospitalarOpcoes = {
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
    series: [
      {
        type: 'rangeArea',
        name: 'Referência CQH',
        data: dadosPacientesDia.map((el) => {
          const data = el["Data"];
          return {
            x: data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4),
            y: [0.75, 0.85],
          };
        }),
      },
      {
        type: 'rangeArea',
        name: 'Referência Brasil',
        data: dadosPacientesDia.map((el) => {
          const data = el["Data"];
          return {
            x: data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4),
            y: [0.8, 0.85],
          };
        }),
      },
      {
        type: 'line',
        name: 'HGR',
        data: Array.from({ length: dadosPacientesDia.length }, (_, i) => {
          const data = dadosPacientesDia[i]["Data"];
          const ipacientesDias = Object.values(dadosPacientesDiaPorSetor).reduce((acc, cur) => {
            return acc + (cur.data[i] === null ? 0 : cur.data[i]);
          }, 0);
          const ileitosDias = Object.values(dadosLeitosDiaPorSetor).reduce((acc, cur) => {
            return acc + (cur.data[i] === null ? 0 : cur.data[i]);
          }, 0);

          return {
            x: data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4),
            y: ipacientesDias / (ileitosDias === 0 ? 1 : ileitosDias),
          };
        }),
      }
    ],
    chart: {
      height: 350,
      type: 'rangeArea',
      animations: {
        speed: 500
      },
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: true,
      enabledOnSeries: [2],
      formatter: (val) => {
        return percentFormatter.format(val);
      }
    },
    fill: {
      opacity: [0.25, 0.25, 1]
    },
    stroke: {
      width: [0, 0, 2]
    },
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value) {
          return percentFormatter.format(value);
        }
      }
    },
    xaxis: {
      title: {
        text: 'Meses',
      },
    },
    markers: {
      size: 0
    },
    yaxis: [
      {
        title: {
          text: 'Taxa',
        },
        labels: {
          formatter: (val) => {
            return percentFormatter.format(val);
          }
        },
      },
    ],
  };

  var giroDeLeitoOpcoes = {
    series: [{
      name: "HGR",
      data: Array.from({ length: dadosSaidasPorDia.length }, (_, i) => {
        const iSaidasDia = Object.values(dadosSaidasPorDiaPorSetor).reduce((acc, cur) => {
          return acc + (cur.data[i] === null ? 0 : cur.data[i]);
        }, 0);
        const iLeitosDia = Object.values(dadosLeitosDiaPorSetor).reduce((acc, cur) => {
          return acc + (cur.data[i] === null ? 0 : cur.data[i]);
        }, 0);

        return numberLiteralFormatter.format(iSaidasDia / (iLeitosDia === 0 ? 1 : iLeitosDia));
      }),
    }],
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosSaidasPorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value) {
          return numberFormatter.format(value === null ? 0 : value);
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  var mediaDePermanenciaOpcoes = {
    series: [{
      name: "HGR",
      data: Array.from({ length: dadosPacientesDia.length }, (_, i) => {
        const iPacientesDia = Object.values(dadosPacientesDiaPorSetor).reduce((acc, cur) => {
          return acc + (cur.data[i] === null ? 0 : cur.data[i]);
        }, 0);
        const iSaidasDia = Object.values(dadosSaidasPorDiaPorSetor).reduce((acc, cur) => {
          return acc + (cur.data[i] === null ? 0 : cur.data[i]);
        }, 0);

        return numberLiteralFormatter.format(iPacientesDia / (iSaidasDia === 0 ? 1 : iSaidasDia));
      }),
    }],
    chart: {
      height: 350,
      type: 'bar',
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        dataLabels: {
          total: {
            enabled: true,
            style: {
              fontSize: '13px',
              fontWeight: 900
            }
          }
        }
      },
    },
    stroke: {
      width: 3,
    },
    fill: {
      type: 'solid',
      opacity: 1,
    },
    labels: dadosSaidasPorDia.map((el) => {
      const data = el["Data"];
      return data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4)
    }),
    markers: {
      size: 0
    },
    xaxis: {
      title: {
        text: 'Dias',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Pacientes',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value) {
          return numberFormatter.format(value === null ? 0 : value);
        }
      }
    },
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
  };

  var intervaloSubstituicaoLeitoOpcoes = {
    legend: {
      position: 'top',
      showForSingleSeries: true,
    },
    series: [
      {
        type: 'line',
        name: 'Referência Brasil',
        data: dadosPacientesDia.map((el) => {
          const data = el["Data"];
          return {
            x: data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4),
            y: 79,
          };
        }),
      },
      {
        type: 'line',
        name: 'HGR',
        data: Array.from({ length: dadosPacientesDia.length }, (_, i) => {
          const iDadosPacientesDiaPorSetor = { ...dadosPacientesDiaPorSetor };
          const iDadosLeitosDiaPorSetor = { ...dadosLeitosDiaPorSetor };
          const iDadosSaidasPorDiaPorSetor = { ...dadosSaidasPorDiaPorSetor };

          const data = dadosPacientesDia[i]["Data"];
          const iPacientesDias = Object.values(iDadosPacientesDiaPorSetor).reduce((acc, cur) => {
            return acc + (cur.data[i] === null ? 0 : cur.data[i]);
          }, 0);
          const iLeitosDias = Object.values(iDadosLeitosDiaPorSetor).reduce((acc, cur) => {
            return acc + (cur.data[i] === null ? 0 : cur.data[i]);
          }, 0);
          const iSaidasDia = Object.values(iDadosSaidasPorDiaPorSetor).reduce((acc, cur) => {
            return acc + (cur.data[i] === null ? 0 : cur.data[i]);
          }, 0);

          const taxaDeOcupacao = iPacientesDias / (iLeitosDias === 0 ? 1 : iLeitosDias);
          const mediaDePermanencia = iPacientesDias / (iSaidasDia === 0 ? 1 : iSaidasDia);

          return {
            x: data.substring(8, 10) + "/" + data.substring(5, 7) + "/" + data.substring(0, 4),
            y: (((1 - taxaDeOcupacao) * mediaDePermanencia) / (taxaDeOcupacao === 0 ? 1 : taxaDeOcupacao)) * 24,
          };
        }),
      }
    ],
    chart: {
      height: 350,
      type: 'rangeArea',
      animations: {
        speed: 500
      },
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: true,
      enabledOnSeries: [1],
      formatter: (val) => {
        return numberFormatter.format(val);
      }
    },
    fill: {
      opacity: [1, 1]
    },
    stroke: {
      width: [2, 2]
    },
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: function(value) {
          return numberFormatter.format(value);
        }
      }
    },
    xaxis: {
      title: {
        text: 'Meses',
      },
    },
    yaxis: [
      {
        title: {
          text: 'Dias',
        },
        labels: {
          formatter: (val) => {
            return numberFormatter.format(val);
          }
        },
      },
    ],
  };

  const leitosDia = new ApexCharts(
    document.querySelector("#leitos-dia"),
    leitosDiaOpcoes,
  );
  leitosDia.render();

  const pacientesDia = new ApexCharts(
    document.querySelector("#pacientes-dia"),
    pacientesDiaOpcoes,
  );
  pacientesDia.render();

  const entradasPorDia = new ApexCharts(
    document.querySelector("#entradas-por-dia"),
    entradasPorDiaOpcoes,
  );
  entradasPorDia.render();

  const cirurgiasPorDia = new ApexCharts(
    document.querySelector("#cirurgias-por-dia"),
    cirurgiasPorDiaOpcoes,
  );
  cirurgiasPorDia.render();

  const entradasPreCirurgicasPorDia = new ApexCharts(
    document.querySelector("#entradas-pre-cirurgicas-por-dia"),
    entradasPreCirurgicasPorDiaOpcoes,
  );
  entradasPreCirurgicasPorDia.render();

  const saidasPorDiaPorSetor = new ApexCharts(
    document.querySelector("#saidas-por-dia-por-setor"),
    saidasPorDiaPorSetorOpcoes,
  );
  saidasPorDiaPorSetor.render();

  const saidasPorDiaPorTipoDeSaida = new ApexCharts(
    document.querySelector("#saidas-por-dia-por-tipo-de-saida"),
    saidasPorDiaPorTipoDeSaidaOpcoes,
  );
  saidasPorDiaPorTipoDeSaida.render();

  const saidasAntes24PorDiaPorSetor = new ApexCharts(
    document.querySelector("#saidas-antes-24-por-dia-por-setor"),
    saidasAntes24PorDiaPorSetorOpcoes,
  );
  saidasAntes24PorDiaPorSetor.render();

  const saidasAntes24PorDiaPorTipoDeSaida = new ApexCharts(
    document.querySelector("#saidas-antes-24-por-dia-por-tipo-de-saida"),
    saidasAntes24PorDiaPorTipoDeSaidaOpcoes,
  );
  saidasAntes24PorDiaPorTipoDeSaida.render();

  const saidasDepois24PorDiaPorSetor = new ApexCharts(
    document.querySelector("#saidas-depois-24-por-dia-por-setor"),
    saidasDepois24PorDiaPorSetorOpcoes,
  );
  saidasDepois24PorDiaPorSetor.render();

  const saidasDepois24PorDiaPorTipoDeSaida = new ApexCharts(
    document.querySelector("#saidas-depois-24-por-dia-por-tipo-de-saida"),
    saidasDepois24PorDiaPorTipoDeSaidaOpcoes,
  );
  saidasDepois24PorDiaPorTipoDeSaida.render();

  const saidasPosCirurgicasPorDiaPorSetor = new ApexCharts(
    document.querySelector("#saidas-pos-cirurgicas-por-dia-por-setor"),
    saidasPosCirurgicasPorDiaPorSetorOpcoes,
  );
  saidasPosCirurgicasPorDiaPorSetor.render();

  const saidasPosCirurgicasPorDiaPorTipoDeSaida = new ApexCharts(
    document.querySelector("#saidas-pos-cirurgicas-por-dia-por-tipo-de-saida"),
    saidasPosCirurgicasPorDiaPorTipoDeSaidaOpcoes,
  );
  saidasPosCirurgicasPorDiaPorTipoDeSaida.render();

  const taxaEfetividadeCirurgica = new ApexCharts(
    document.querySelector("#taxa-efetividade-cirurgica"),
    cirurgiasBemSucedidasPorDiaOpcoes,
  );
  taxaEfetividadeCirurgica.render();

  const transferenciasEnviadasPorSetor = new ApexCharts(
    document.querySelector("#transferencias-enviadas"),
    transferenciasEnviadasPorSetorOpcoes,
  );
  transferenciasEnviadasPorSetor.render();

  const transferenciasRecebidasPorSetor = new ApexCharts(
    document.querySelector("#transferencias-recebidas"),
    transferenciasRecebidasPorSetorOpcoes,
  );
  transferenciasRecebidasPorSetor.render();

  const taxaDeOcupacaoHospitalar = new ApexCharts(
    document.querySelector("#taxa-de-ocupacao-hospitalar"),
    taxaDeOcupacaoHospitalarOpcoes,
  );
  taxaDeOcupacaoHospitalar.render();

  const giroDeLeito = new ApexCharts(
    document.querySelector("#giro-de-leito"),
    giroDeLeitoOpcoes,
  );
  giroDeLeito.render();

  const mediaDePermanencia = new ApexCharts(
    document.querySelector("#media-de-permanencia"),
    mediaDePermanenciaOpcoes,
  );
  mediaDePermanencia.render();

  const intervaloSubstituicaoLeito = new ApexCharts(
    document.querySelector("#intervalo-substituicao-leito"),
    intervaloSubstituicaoLeitoOpcoes,
  );
  intervaloSubstituicaoLeito.render();
});
