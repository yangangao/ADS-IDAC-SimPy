// Echarts树 结点点击事件
ec_tree.on('click', function (params) {
    // 控制台打印数据的名称
    // alert("value:"+params.value + " dataIndex:"+params.dataIndex+"\nseriesIndex:"+params.seriesIndex+" seriesName:"+ params.seriesName );
	// , params.seriesIndex, params.seriesName
	$('#dataId').attr('value', params.value);
});

// 清除绘图 按钮点击事件
$("#clearPolyline").click(function(event) {
	// alert("clear polyline")
	map.clearOverlays()
});

// 测试动态更新VO图 点击事件
$("#testDynamicImg").click(function(event) {
	updateVoImg("ship0");
});

// 绘制动态绘制polyLine 按钮点击事件
$("#drawPolyline").click(function(event) {
	// var pois = [
	// 	new BMap.Point(122.326654, 31.110672),
	// 	new BMap.Point(122.216654, 31.110672),
	// 	new BMap.Point(122.146654, 31.210672),
	// 	new BMap.Point(122.426654, 31.260672),
	// ];
	var pois = get_pois();

	// my_add_polyline(pois);
	// setTimeout(function(){
	// 	my_add_polyline(pois2);
	// 	setTimeout(function(){
	// 		my_add_polyline(pois3);
	// 	}, 1000);
	// }, 1000);

	draw_dynamic_polyLine(pois);
});

// 获取用于绘制polyLine的数据集合（数组）
function get_pois(){
	return ([[
		new BMap.Point(122.326654, 31.110672),
		new BMap.Point(122.216654, 31.110672),
		new BMap.Point(122.146654, 31.210672),
		new BMap.Point(122.426654, 31.260672),
	],[
		new BMap.Point(122.226654, 31.210672),
		new BMap.Point(122.316654, 31.210672),
		new BMap.Point(122.346654, 31.310672),
		new BMap.Point(122.226654, 31.260672),
	]]);
}

// 动态绘制polyLine功能函数
function draw_dynamic_polyLine(pois) {
	//感谢杨总
	my_add_polyline([pois[0][0], pois[0][1]]);
	my_add_polyline([pois[1][0], pois[1][1]]);
	updateVoImg("ship0")
	console.log(0, pois[0][0], pois[0][1]);
	var lineDataIndex = 1;
	if (pois[0].length > 0) {
		var intervalId = setInterval(() => {
			if (lineDataIndex == pois[0].length - 1) {
				clearInterval(intervalId);
				// console.log("this is clearInterval.");
			}
			if (lineDataIndex < pois[0].length - 1) {
				my_add_polyline([pois[0][lineDataIndex], pois[0][lineDataIndex + 1]]);
				my_add_polyline([pois[1][lineDataIndex], pois[1][lineDataIndex + 1]]);
				updateVoImg("ship"+lineDataIndex.toString())
				console.log(lineDataIndex, pois[0][lineDataIndex], pois[0][lineDataIndex + 1]);
			}
			lineDataIndex++;
		}, 2000);
	}
}

// 更新VO图功能函数
function updateVoImg(imgName){
	// imgName: String
	imgUrl = "/img/"+ imgName.toString();
	// imgUrl = "/img/"+ imgName;
	// 方式1：DOM操作img 属性
	$('#voImg').attr('src', imgUrl);
	
	// 方式2 Ajax方式
	// $.ajax('', {
	// 	url: imgUrl,
	// 	success:function(data){
	// 		$('#voImg').attr('src', "data:image/png;base64,"+data);
	// 	},
	// 	error:function(xhr,type,errorThrown){
	// 		alert(error);
	// 	}
	// });
}