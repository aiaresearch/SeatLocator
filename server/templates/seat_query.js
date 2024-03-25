let debug = true;

function update_seat_num(n_available, n_total, id) {
  // let available_seat_element = document.getElementById('available-seats');
  // let total_seat_element = document.getElementById('total-seats');
  let container = document.getElementById(id);
  console.log(id);
  let available_seat_element = container.querySelector('.available-seats');
  let total_seat_element = container.querySelector('.total-seats');
  available_seat_element.innerHTML = n_available;
  total_seat_element.innerHTML = n_total;
};

// 点击事件处理函数 - 查询总座位信息
function queryTotalSeats() {
  if (!debug) {
    // 使用 fetch 发送 GET 请求获取总座位信息
    fetch('/query', {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    })
      .then(response => response.json()) // 解析响应为 JSON 格式
      .then(data => {
        // TODO: Refresh seat data
        update_seat_num(data.all_available_value, data.all_total_value);
      })
      .catch(error => {
        // 处理错误
        console.error('Error:', error);
        // 在页面上显示错误信息
        var totalSeatInfoElement = document.getElementById('totalSeatInfo');
        totalSeatInfoElement.textContent = '总座位信息获取失败';
      });
  }
  if (debug) {
    // TODO Generate random data
    let all_available_value = 10;
    let all_total_value = 10;

    update_seat_num(all_available_value, all_total_value, "totalSeatInfo");
  }
}

// 点击事件处理函数 - 查询分楼座位信息
function queryFloorSeats() {
  if (!debug) {
    // 使用 fetch 发送 GET 请求获取分楼座位信息
    fetch('/query', {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    })
      .then(response => response.json()) // 解析响应为 JSON 格式
      .then(data => {
        // 处理服务器返回的分楼座位信息，并显示在页面上
        var floorSeatInfoElement = document.getElementById('floorSeatInfo');
        floorSeatInfoElement.innerHTML = `
    <p>A区域可用座位数：<span class="available-seats">${data.floor1_available_value}</span> / ${data.floor1_total_value}</p>
    <p><span class="timetext">数据更新截止至</span><span class="timestamp">${data.timestamp_1}</span><p>
    <p>B区域可用座位数：<span class="available-seats">${data.floor2_available_value}</span> / ${data.floor2_total_value}</p>
    <p><span class="timetext">数据更新截止至</span><span class="timestamp">${data.timestamp_2}</span><p>
  `;
        // 显示分楼座位信息容器
        floorSeatInfoElement.style.display = 'block';
      })
      .catch(error => {
        // 处理错误
        console.error('Error:', error);
        // 在页面上显示错误信息
        var floorSeatInfoElement = document.getElementById('floorSeatInfo');
        floorSeatInfoElement.textContent = '座位信息获取失败';
      });
  }
  if (debug) {
    /*
    // 显示分楼座位信息
    var floorSeatInfoElement = document.getElementById('floorSeatInfo');
    floorSeatInfoElement.innerHTML = `
          <p>A区域可用座位数：<span class="available-seats">${3}</span> / ${3}</p>
          <p><span class="timetext">数据更新截止至</span><span class="timestamp">${33}</span><p>
          <p>B区域可用座位数：<span class="available-seats">${3}</span> / ${33}</p>
          <p><span class="timetext">数据更新截止至</span><span class="timestamp">${33}</span><p>
        `;
    // 显示分楼座位信息容器
    floorSeatInfoElement.style.display = 'block';*/
    // TODO Generate random data
    let floor1_available_value = 10;
    let floor1_total_value = 10;
    let floor2_available_value = 10;
    let floor2_total_value = 10;
    let timestamp_1 = 10;
    let timestamp_2 = 10;
    update_seat_num(floor1_available_value, floor1_total_value, timestamp_1, 'floor-a');
    update_seat_num(floor2_available_value, floor2_total_value, timestamp_2, 'floor-b');
  }
}

document.addEventListener("DOMContentLoaded", function () {

  function refreshdata() {
    queryTotalSeats();
    queryFloorSeats();
  }

  refreshdata();

  setInterval(refreshdata, 5000); // Refresh data every 5 seconds

});
