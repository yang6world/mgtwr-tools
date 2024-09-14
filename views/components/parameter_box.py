from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QCheckBox, QSpinBox


def creat_gtwr_param_box(param_layout):
    # GTWR 参数

    # 收敛公差
    tol_label = QLabel("收敛公差")
    tol_input = QLineEdit()
    tol_input.setToolTip("控制模型收敛的公差（默认值为1.0e-6）")
    tol_input.setText("1.0e-6")
    tol_layout = QHBoxLayout()
    tol_layout.addWidget(tol_label)
    tol_layout.addWidget(tol_input)

    # 最大迭代次数
    max_iter_label = QLabel("最大迭代次数")
    max_iter_input = QLineEdit()
    max_iter_input.setToolTip("模型的最大迭代次数（默认值为200）")
    max_iter_input.setText("200")
    # 设置只能输入整数
    max_iter_input.setValidator(QIntValidator(1, 1000))
    max_iter_layout = QHBoxLayout()
    max_iter_layout.addWidget(max_iter_label)
    max_iter_layout.addWidget(max_iter_input)

    # 带宽小数点精度
    bw_decimal_label = QLabel("带宽精度")
    bw_decimal_input = QLineEdit()
    bw_decimal_input.setToolTip("指定带宽的小数点精度（默认值为1）")
    bw_decimal_input.setText("1")
    # 设置只能输入整数
    bw_decimal_input.setValidator(QIntValidator(0, 10))
    bw_decimal_layout = QHBoxLayout()
    bw_decimal_layout.addWidget(bw_decimal_label)
    bw_decimal_layout.addWidget(bw_decimal_input)

    # 时空尺度小数点精度
    tau_decimal_label = QLabel("时空尺度精度")
    tau_decimal_input = QLineEdit()
    tau_decimal_input.setToolTip("指定时空尺度的小数点精度（默认值为1）")
    tau_decimal_input.setText("1")
    # 设置只能输入整数
    tau_decimal_input.setValidator(QIntValidator(0, 10))
    tau_decimal_layout = QHBoxLayout()
    tau_decimal_layout.addWidget(tau_decimal_label)
    tau_decimal_layout.addWidget(tau_decimal_input)

    # 将所有参数放入一个水平布局
    param_combined_layout = QHBoxLayout()
    param_combined_layout.addLayout(tol_layout)
    param_combined_layout.addLayout(max_iter_layout)
    param_combined_layout.addLayout(bw_decimal_layout)
    param_combined_layout.addLayout(tau_decimal_layout)
    param_layout.addLayout(param_combined_layout)

    # 带宽最小值
    bw_min_label = QLabel("带宽最小值")
    bw_min_input = QLineEdit()
    bw_min_input.setToolTip("模型使用的带宽最小值")
    # 设置只能输入浮点数
    bw_min_input.setValidator(QDoubleValidator(0.0, 9999.9, 3))
    bw_min_layout = QHBoxLayout()
    bw_min_layout.addWidget(bw_min_label)
    bw_min_layout.addWidget(bw_min_input)

    # 带宽最大值
    bw_max_label = QLabel("带宽最大值")
    bw_max_input = QLineEdit()
    bw_max_input.setToolTip("模型使用的带宽最大值")
    # 设置只能输入浮点数
    bw_max_input.setValidator(QDoubleValidator(0.0, 9999.9, 3))
    bw_max_layout = QHBoxLayout()
    bw_max_layout.addWidget(bw_max_label)
    bw_max_layout.addWidget(bw_max_input)

    # 将带宽布局添加到主布局
    bw_combined_layout = QHBoxLayout()
    bw_combined_layout.addLayout(bw_min_layout)
    bw_combined_layout.addLayout(bw_max_layout)
    param_layout.addLayout(bw_combined_layout)

    # 时空尺度最小值
    tau_min_label = QLabel("时空尺度最小值")
    tau_min_input = QLineEdit()
    tau_min_input.setToolTip("模型使用的时空尺度最小值")
    # 设置只能输入浮点数
    tau_min_input.setValidator(QDoubleValidator(0.0, 9999.9, 3))
    tau_min_layout = QHBoxLayout()
    tau_min_layout.addWidget(tau_min_label)
    tau_min_layout.addWidget(tau_min_input)

    # 时空尺度最大值
    tau_max_label = QLabel("时空尺度最大值")
    tau_max_input = QLineEdit()
    tau_max_input.setToolTip("模型使用的时空尺度最大值")
    # 设置只能输入浮点数
    tau_max_input.setValidator(QDoubleValidator(0.0, 9999.9, 3))
    tau_max_layout = QHBoxLayout()
    tau_max_layout.addWidget(tau_max_label)
    tau_max_layout.addWidget(tau_max_input)

    # 将时空尺度布局添加到主布局
    tau_combined_layout = QHBoxLayout()
    tau_combined_layout.addLayout(tau_min_layout)
    tau_combined_layout.addLayout(tau_max_layout)
    param_layout.addLayout(tau_combined_layout)

    # 保存动态输入的引用
    return {
        'bw_min': bw_min_input,
        'bw_max': bw_max_input,
        'tau_min': tau_min_input,
        'tau_max': tau_max_input,
        'tol': tol_input,
        'bw_decimal': bw_decimal_input,
        'tau_decimal': tau_decimal_input,
        'max_iter': max_iter_input,
    }


def creat_mgtwr_param_box(param_layout):
    # MGTWR 参数
    # 收敛公差 (tol)
    tol_label = QLabel("收敛公差")
    tol_input = QLineEdit()
    tol_input.setToolTip("控制模型收敛的公差（默认值为1.0e-6）")
    tol_input.setText("1.0e-6")
    tol_layout = QHBoxLayout()
    tol_layout.addWidget(tol_label)
    tol_layout.addWidget(tol_input)

    # 带宽搜索收敛公差 (tol_multi)
    tol_multi_label = QLabel("多带宽算法收敛公差")
    tol_multi_input = QLineEdit()
    tol_multi_input.setToolTip("控制多带宽算法收敛的公差（默认值为1.0e-5）")
    tol_multi_input.setText("1.0e-5")
    tol_multi_layout = QHBoxLayout()
    tol_multi_layout.addWidget(tol_multi_label)
    tol_multi_layout.addWidget(tol_multi_input)

    # 残差平方和评价标准 (rss_score)
    rss_score_label = QLabel("使用残差平方和")
    rss_score_input = QCheckBox()
    rss_score_layout = QHBoxLayout()
    rss_score_layout.addWidget(rss_score_label)
    rss_score_layout.addWidget(rss_score_input)

    tol_tol_multi_combined_layout = QHBoxLayout()
    tol_tol_multi_combined_layout.addLayout(tol_layout)
    tol_tol_multi_combined_layout.addLayout(tol_multi_layout)
    tol_tol_multi_combined_layout.addLayout(rss_score_layout)
    param_layout.addLayout(tol_tol_multi_combined_layout)

    # 带宽小数位数 (bw_decimal)
    bw_decimal_label = QLabel("带宽小数位数")
    bw_decimal_input = QSpinBox()
    bw_decimal_input.setMinimum(0)
    bw_decimal_input.setMaximum(10)
    bw_decimal_input.setValue(1)
    bw_decimal_layout = QHBoxLayout()
    bw_decimal_layout.addWidget(bw_decimal_label)
    bw_decimal_layout.addWidget(bw_decimal_input)

    # 时空尺度小数位数 (tau_decimal)
    tau_decimal_label = QLabel("时空尺度小数位数")
    tau_decimal_input = QSpinBox()
    tau_decimal_input.setMinimum(0)
    tau_decimal_input.setMaximum(10)
    tau_decimal_input.setValue(1)
    tau_decimal_layout = QHBoxLayout()
    tau_decimal_layout.addWidget(tau_decimal_label)
    tau_decimal_layout.addWidget(tau_decimal_input)

    # 带宽和时空尺度的小数位布局
    decimal_combined_layout = QHBoxLayout()
    decimal_combined_layout.addLayout(bw_decimal_layout)
    decimal_combined_layout.addLayout(tau_decimal_layout)
    param_layout.addLayout(decimal_combined_layout)

    # bw
    bw_min_label = QLabel("带宽最小值")
    bw_min_input = QLineEdit()
    bw_min_input.setToolTip("带宽搜索的最小值")
    bw_min_input.setPlaceholderText("None")
    bw_min_layout = QHBoxLayout()
    bw_min_layout.addWidget(bw_min_label)
    bw_min_layout.addWidget(bw_min_input)

    bw_max_label = QLabel("带宽最大值")
    bw_max_input = QLineEdit()
    bw_max_input.setToolTip("带宽搜索的最大值")
    bw_max_input.setPlaceholderText("None")
    bw_max_layout = QHBoxLayout()
    bw_max_layout.addWidget(bw_max_label)
    bw_max_layout.addWidget(bw_max_input)
    # tau
    tau_min_label = QLabel("时空尺度最小值")
    tau_min_input = QLineEdit()
    tau_min_input.setToolTip("时空尺度搜索的最小值")
    tau_min_input.setPlaceholderText("None")
    tau_min_layout = QHBoxLayout()
    tau_min_layout.addWidget(tau_min_label)
    tau_min_layout.addWidget(tau_min_input)

    tau_max_label = QLabel("时空尺度最大值")
    tau_max_input = QLineEdit()
    tau_max_input.setToolTip("时空尺度搜索的最大值")
    tau_max_input.setPlaceholderText("None")
    tau_max_layout = QHBoxLayout()
    tau_max_layout.addWidget(tau_max_label)
    tau_max_layout.addWidget(tau_max_input)

    bw_tau_combined_layout = QHBoxLayout()
    bw_tau_combined_layout.addLayout(bw_min_layout)
    bw_tau_combined_layout.addLayout(bw_max_layout)
    bw_tau_combined_layout.addLayout(tau_min_layout)
    bw_tau_combined_layout.addLayout(tau_max_layout)
    param_layout.addLayout(bw_tau_combined_layout)

    # 多带宽最小值 (multi_bw_min)
    multi_bw_min_label = QLabel("多带宽最小值")
    multi_bw_min_input = QLineEdit()
    multi_bw_min_input.setPlaceholderText('多个值用逗号分隔')
    multi_bw_min_input.setToolTip("多带宽算法的带宽搜索范围,可以是多个值，用逗号分隔")
    multi_bw_min_layout = QHBoxLayout()
    multi_bw_min_layout.addWidget(multi_bw_min_label)
    multi_bw_min_layout.addWidget(multi_bw_min_input)

    # 多带宽最大值 (multi_bw_max)
    multi_bw_max_label = QLabel("多带宽最大值")
    multi_bw_max_input = QLineEdit()
    multi_bw_max_input.setPlaceholderText('多个值用逗号分隔')
    multi_bw_max_input.setToolTip("多带宽算法的带宽搜索范围,可以是多个值，用逗号分隔")
    multi_bw_max_layout = QHBoxLayout()
    multi_bw_max_layout.addWidget(multi_bw_max_label)
    multi_bw_max_layout.addWidget(multi_bw_max_input)

    # 将两个多带宽的输入框放到一个总的水平布局中
    multi_bw_combined_layout = QHBoxLayout()
    multi_bw_combined_layout.addLayout(multi_bw_min_layout)
    multi_bw_combined_layout.addLayout(multi_bw_max_layout)
    param_layout.addLayout(multi_bw_combined_layout)

    # 多时空尺度最小值 (multi_tau_min)
    multi_tau_min_label = QLabel("多时空尺度最小值")
    multi_tau_min_input = QLineEdit()
    multi_tau_min_input.setPlaceholderText('多个值用逗号分隔')
    multi_tau_min_input.setToolTip("多带宽算法的时空尺度搜索范围,可以是多个值，用逗号分隔")
    multi_tau_min_layout = QHBoxLayout()
    multi_tau_min_layout.addWidget(multi_tau_min_label)
    multi_tau_min_layout.addWidget(multi_tau_min_input)

    # 多时空尺度最大值 (multi_tau_max)
    multi_tau_max_label = QLabel("多时空尺度最大值")
    multi_tau_max_input = QLineEdit()
    multi_tau_max_input.setPlaceholderText('多个值用逗号分隔')
    multi_tau_max_input.setToolTip("多带宽算法的时空尺度搜索范围,可以是多个值，用逗号分隔")
    multi_tau_max_layout = QHBoxLayout()
    multi_tau_max_layout.addWidget(multi_tau_max_label)
    multi_tau_max_layout.addWidget(multi_tau_max_input)

    # 将两个多时空尺度的输入框放到一个总的水平布局中
    multi_tau_combined_layout = QHBoxLayout()
    multi_tau_combined_layout.addLayout(multi_tau_min_layout)
    multi_tau_combined_layout.addLayout(multi_tau_max_layout)
    param_layout.addLayout(multi_tau_combined_layout)

    # 初始带宽 (init_bw)
    init_bw_label = QLabel("初始带宽")
    init_bw_input = QLineEdit()
    init_bw_input.setPlaceholderText('一般为空')
    init_bw_label.setToolTip("MGTWR模型的带宽，如果为空则从MGTWR模型派生")
    init_bw_layout = QHBoxLayout()
    init_bw_layout.addWidget(init_bw_label)
    init_bw_layout.addWidget(init_bw_input)

    # 初始时空尺度 (init_tau)
    init_tau_label = QLabel("初始时空尺度")
    init_tau_input = QLineEdit()
    init_tau_input.setPlaceholderText('一般为空')
    init_tau_label.setToolTip("MGTWR模型的时空尺度，如果为空则从MGTWR模型派生")
    init_tau_layout = QHBoxLayout()
    init_tau_layout.addWidget(init_tau_label)
    init_tau_layout.addWidget(init_tau_input)

    init_bw_tau_combined_layout = QHBoxLayout()
    init_bw_tau_combined_layout.addLayout(init_bw_layout)
    init_bw_tau_combined_layout.addLayout(init_tau_layout)
    param_layout.addLayout(init_bw_tau_combined_layout)

    # 返回包含所有输入框的字典
    return {
        'bw_min': bw_min_input,
        'bw_max': bw_max_input,
        'tau_min': tau_min_input,
        'tau_max': tau_max_input,
        'multi_bw_min': multi_bw_min_input,
        'multi_bw_max': multi_bw_max_input,
        'multi_tau_min': multi_tau_min_input,
        'multi_tau_max': multi_tau_max_input,
        'tol': tol_input,
        'bw_decimal': bw_decimal_input,
        'tau_decimal': tau_decimal_input,
        'init_bw': init_bw_input,
        'init_tau': init_tau_input,
        'tol_multi': tol_multi_input,
        'rss_score': rss_score_input,
    }
