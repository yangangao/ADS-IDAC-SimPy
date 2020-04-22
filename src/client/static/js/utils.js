// Echarts树 结点点击事件
ec_tree.on('click', function (params) {
    // 控制台打印数据的名称
    // alert("value:"+params.value + "\n dataIndex:"+params.dataIndex+"\n seriesIndex:"+params.seriesIndex+"\n seriesName:"+ params.seriesName );
	// , params.seriesIndex, params.seriesName

	$('#dataId').attr('value', params.value);
	var vmid = params.value;
	// var vmid = "2004022208011387";
	getVMData(vmid);
	showShipInfo();
	// getVMData(vmid, function(err, data){
	// 	console.log("VMData callback 测试: ", data);
		
	// });
	
	// console.log("测试调用之后VMData: ", mysimdata);
	// draw_dynamic_polyLine(VMData);
	
	//动态绘图
	// var pois = get_pois();
	// draw_dynamic_polyLine(pois);
});

ec_tree.on('contextmenu', function (params) {
	// alert('contextmenu')
	// window.open('https://www.baidu.com/s?wd=' + encodeURIComponent(params.name));
	// 发送被点击的节点回去
	// var treeid = document.getElementById('treeId').value;
	$('#dataId').attr('value', params.value);
	branchUrl = "/tree/branch/" + params.value.toString();
	// alert(branchUrl)
	var endin = 4;
	var routs = Array();
	$.ajax('', {
		url: branchUrl,
		dataType:"json",
		success:function(data){
			// alert(data.in1);
			showShipInfo();
			endin = data.endin;
			// 这里埋了一个BUG！！！最多只能六层。  JSON->JS数组
			routs = new Array(data.in1,data.in2,data.in3,data.in4,data.in5,data.in6);
			// alert(routs);
			for (var i = 1; i <= endin; i++){ 
				getVMData(routs[i - 1]);
				// alert(routs[i - 1])
			}
		},
		error:function(xhr,type,errorThrown){
			alert(error);
		}
	});
	// 收到一系列节点后
	// 开始系列绘图
	for (var i = 1; i <= endin; i++){ 
		getVMData(routs[i - 1]);
		alert(routs[i - 1])
	}
});

	// 自定义参数 确认 按钮点击事件
$("#user_confirm").click(function(event) {
	getUserParameter();
	hideShipInfo();
});


// // 切换为英文 按钮点击事件
// $("#S2E").click(function(event) {
// 	window.location.href="/en_version"
// });
// // 切换为中文 按钮点击事件
// $("#S2Z").click(function(event) {
// });

// 清除绘图 按钮点击事件
$("#clearPolyline").click(function(event) {
	// alert("clear polyline")
	hideShipInfo();
	map.clearOverlays();
});

// 测试动态更新VO图 点击事件
$("#testDynamicImg").click(function(event) {
	updateVoImg("1000010086312797");
	// 方式2 Ajax方式
	// $.ajax('', {
	// 	url: "/testS2F/1000010086312797",
	// 	success:function(data){
	// 		console.log("data: ", data)
	// 		$('#voImg').attr('src', "data:image/png;base64,"+data);
	// 	},
	// 	error:function(xhr,type,errorThrown){
	// 		alert(error);
	// 	}
	// });
});

// 获取最新仿真树
$("#getSimTree").click(function(event) {
	// 先清理掉当前的绘图PolyLine
	map.clearOverlays();
	hideShipInfo();
	ec_tree.showLoading();
	// TODO
	// var treeid = "Tree2004022208017821";
	// var treeid = "Tree2004022316511498";
	// treeUrl = "/tree/" + treeid;
	lastestTreeUrl = "/tree/lastest";
	$.ajax('', {
		url: lastestTreeUrl,
		dataType:"json",
		success:function(data){
			ec_tree_option.series[0].data = data.TREEData.data;
			ec_tree.hideLoading();
			ec_tree.setOption(ec_tree_option);
			// 将TREEID填写到treeId输入框中
			$('#treeId').attr('value', data.TREEID);
		},
		error:function(xhr,type,errorThrown){
			alert(error);
		}
	});
});

// 绘制动态绘制polyLine 按钮点击事件
// $("#drawPolyline").click(function(event) {
	// var pois = [
	// 	new BMap.Point(122.326654, 31.110672),
	// 	new BMap.Point(122.216654, 31.110672),
	// 	new BMap.Point(122.146654, 31.210672),
	// 	new BMap.Point(122.426654, 31.260672),
	// ];
	// var pois = get_pois();

	// my_add_polyline(pois);
	// setTimeout(function(){
	// 	my_add_polyline(pois2);
	// 	setTimeout(function(){
	// 		my_add_polyline(pois3);
	// 	}, 1000);
	// }, 1000);

// 	draw_dynamic_polyLine(pois);
// });

// 获取用于绘制polyLine的数据集合（数组）
// function get_pois(){
// 	return ([[
// 		new BMap.Point(122.326654, 31.110672),
// 		new BMap.Point(122.216654, 31.110672),
// 		new BMap.Point(122.146654, 31.210672),
// 		new BMap.Point(122.426654, 31.260672),
// 	],[
// 		new BMap.Point(122.226654, 31.210672),
// 		new BMap.Point(122.316654, 31.210672),
// 		new BMap.Point(122.346654, 31.310672),
// 		new BMap.Point(122.226654, 31.260672),
// 	]]);
// }

// 动态绘制polyLine功能函数
// 目前的是绘制两条船
// 感谢杨总 倾情相助
function draw_dynamic_polyLine(pois, Voarr) {
	// 首先将初始位置的点添加进去
	// console.log('Voarr传入参数测试：', Voarr);
	my_add_polyline([pois[0][0], pois[0][1]]);
	my_add_polyline([pois[1][0], pois[1][1]]);
	updateVoImg(Voarr[0])
	// console.log(0, pois[0][0], pois[0][1]);
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
				updateVoImg(Voarr[lineDataIndex])
				// console.log(lineDataIndex, pois[0][lineDataIndex], pois[0][lineDataIndex + 1]);
			}
			lineDataIndex++;
		}, 1000);
	}
	updateVoImg(Voarr[pois[0].length-1])
}

// 更新VO图功能函数
function updateVoImg(imgName){
	console.log("imgName: ", imgName)
	// imgName: String
	// imgUrl = "/img/"+ imgName.toString();
	
	// TODO: 有毒！！！
	// imgUrl = "/vm/2004071252277034";
	imgUrl = "/img/"+ imgName;
	// 方式1：DOM操作img 属性
	// $('#voImg').attr('src', imgUrl);
	
	// 方式2 Ajax方式
	$.ajax('', {
		url: imgUrl,
		success:function(data){
			// console.log("前端调用测试data:", data)
			$('#voImg').attr('src', "data:image/png;base64,"+data);
		},
		error:function(xhr,type,errorThrown){
			alert(error);
		}
	});
}

// 输入VMID，绘制PolyLine
function getVMData(VMID){
	vmUrl = "/vm/" + VMID.toString();
	$.ajax('', {
		url: vmUrl,
		dataType:"json",
		success:function(data){
			var SimData = data.SimData;
			var shipPos = new Array();
			// console.log("VMData 测试: ", SimData)
			var shipNum = data.SimData[0].length; // 当前虚拟机中船的数量，由于每组中数据的量和格式是一致的，只需要解读第0组即可
			var shipVOImg = new Array(); // 用于保存主船的VOImdID
			// 下面初始化用于绘制PolyLine的array
			for (var i=0; i<shipNum; i++){ 
				shipPos.push(new Array());
				// shipPos[i] 用于记录第i条船的坐标序列
			}
			// console.log('shipPos: ', shipPos)
			for(var moment=0; moment<SimData.length; moment++){ 
				if (SimData[moment][0].VOImgID){
					shipVOImg.push(SimData[moment][0].VOImgID);
				}
				else{
					shipVOImg.push('figure');
				}
				for(var ship=0; ship<SimData[moment].length; ship++){
					shipPos[ship].push(new BMap.Point(SimData[moment][ship].lon, SimData[moment][ship].lat));
					// console.log("lon, lat", SimData[moment][ship].lon, SimData[moment][ship].lat)
				}
			}
			// 从这里开始已经处理好数据，shipPos里面就是可以直接绘制PolyLine的数据了
			// console.log('测试return shipPos: ', shipPos);
			var f = function(){
				return draw_dynamic_polyLine(shipPos, shipVOImg);
			}
			f();
			// return shipPos;
		},
		error:function(xhr,type,errorThrown){
			console.log(error)
			// return [];
			// alert(error);
		}
	});
}

// 得到一组船的参数
function getUserParameter(){
	//得到数据
	var muser_speed = document.getElementById('u37_input').value;
	var muser_location_we = document.getElementById('u38_input').value;
	var muser_location_sn = document.getElementById('u39_input').value;
	if($("#mastership").is(":checked")){
	// if(document.getElementById('mastership').check){
		mastership = 1;
		// alert("1");
	}else{
		mastership = 0;
		// alert('错鸟');
	}
	//判断数据完整
	// console.log(user_speed,user_location_we,user_location_sn);
	if(!muser_speed){
		// alert("参数错误");
		muser_speed = prompt('[主]请输入初始速度','7');
	}
	if(!muser_location_we){
		// alert("参数错误");
		muser_location_we = prompt('[主]请输入初始位置（东西）','123');
	}
	if(!muser_location_sn){
		// alert("参数错误");
		muser_location_sn = prompt('[主]请输入初始（南北）','30.99');
	}
	suser_speed = prompt('[客]请输入初始速度','7');
	suser_location_we = prompt('[客]请输入初始位置（东西）','123.15');
	suser_location_sn = prompt('[客]请输入初始位置（南北）','31.02');
	//发送数据
	var user_parameters = 
	{
		// "mastership" : mastership,
		"muser_speed" : muser_speed,
	    "muser_location_we" : muser_location_we,
		"muser_location_sn" : muser_location_sn,
		"suser_speed" : suser_speed,
	    "suser_location_we" : suser_location_we,
		"suser_location_sn" : suser_location_sn
	}
	hideShipInfo();
	ec_tree.showLoading();
	$.post("/userparameters", user_parameters, 
		function(data){ 
		// 这里的alert可以换成模态对话框
		alert("结果: " + data['errmsg'] + "\n状态: " + data['status']); 
		ec_tree.hideLoading();
	}); 

	// $.ajax({
	// 	url:"http://localhost:5000",
	// 	contentType:"application/json",
	// 	data:JSON.stringify(user_parameters,null,4),
	// 	dataType:"json",
	// 	type:"POST",
	// 	success:function (data) {
	// 		console.log(data);
	// 	}
	// });
	// 	//如果不完整 用弹窗提醒
	// 	alert('请补全参数再确认');
	// 	// var userwarr =document.getElementById("u40");
	// 	// userwarr.style.display="";
	// }	
}

// function refresh_time(){
// 	var time = new Date();
// 	setInterval("document.getElementById('time').textContent=new Date().toLocaleString();", 1000);
//     // document.getElementById('time').textContent = time.toISOString();
// }

// 以下是船舶显示框相关函数
// 待补充位置调整函数
function showShipInfo() {
	obj = document.getElementById('u13');
	obj.style.display = "block";
	obj = document.getElementById('u13s');
	obj.style.display = "block"
}
function hideShipInfo() {
	obj = document.getElementById('u13');
	obj.style.display = "none";
	obj = document.getElementById('u13s');
	obj.style.display = "none";
}


