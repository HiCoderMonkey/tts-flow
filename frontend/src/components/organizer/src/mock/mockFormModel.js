export default {
  formModel: {
    componentsTree: [
      {
        id: 'Root_h1ep',
        componentName: 'Root',
        name: '根组件',
        props: { style: {} },
        children: [
          {
            id: 'Container_sei4',
            condition: true,
            componentName: 'Container',
            name: '容器',
            props: {
              wrap: true,
              col: 1,
              style: { flexFlow: 'row wrap' },
              loading: false
            },
            children: [
              {
                id: 'Text_24qw',
                condition: true,
                componentName: 'SudaText',
                name: '文本',
                props: {
                  title: '文本',
                  content: '这是一段文本',
                  style: {},
                  options: '',
                  isBold: false,
                  delLine: false,
                  underLine: false,
                  fetchRemote: false,
                  remote: { id: null, value: '' },
                  formatRule: ''
                }
              },
              {
                id: 'Button_yyj4',
                condition: true,
                componentName: 'SudaButton',
                name: '按钮',
                props: {
                  content: '按钮',
                  submitKey: 'Button_yyj4',
                  type: 'primary',
                  shape: 'square',
                  size: 'small',
                  style: {},
                  disabled: false,
                  loading: false,
                  block: false
                }
              },
              {
                id: 'Button_yzf5',
                condition: true,
                componentName: 'SudaButton',
                name: '按钮',
                props: {
                  content: '按钮',
                  submitKey: 'Button_yzf5',
                  type: 'primary',
                  shape: 'square',
                  size: 'small',
                  style: {},
                  disabled: false,
                  loading: false,
                  block: false
                }
              }
            ]
          },
          {
            id: 'Image_6lad',
            condition: true,
            componentName: 'SudaImage',
            name: '图片',
            props: {
              title: '图片',
              src: 'https://s3-gzpu.didistatic.com/tiyan-base-store/suda/icon/blank.svg',
              alt: '',
              submitKey: 'Image_6lad',
              style: {}
            }
          },
          {
            id: 'Input_l3l6',
            condition: true,
            componentName: 'Input',
            name: '输入框',
            props: {
              submitKey: 'Input_l3l6',
              title: '输入框标题',
              value: '',
              type: 'text',
              allowClear: false,
              placeholder: '请输入',
              rules: [],
              style: {},
              disabled: false,
              size: 'small',
              showWordLimit: false,
              showTip: false,
              tipContent: '提示文字'
            }
          },
          {
            id: 'Radio_amkc',
            condition: true,
            componentName: 'Radio',
            name: '单选框',
            props: {
              submitKey: 'Radio_amkc',
              title: '单选框标题',
              value: '',
              disabled: false,
              type: 'radio',
              size: 'normal',
              style: {},
              rules: [],
              options: [
                { label: '选项一', value: 1, label1: '测试映射关系' },
                { label: '选项二', value: 2, label1: '测试映射关系二' }
              ],
              fetchRemote: false,
              remote: { id: null, label: '', value: '' },
              showTip: false,
              tipContent: '提示文字'
            }
          },
          {
            id: 'Checkbox_vrip',
            condition: true,
            componentName: 'Checkbox',
            name: '多选框',
            props: {
              title: '多选框标题',
              submitKey: 'Checkbox_vrip',
              value: [],
              disabled: false,
              type: '',
              size: 'small',
              style: {},
              options: [
                { label: '多选一', value: 'value1' },
                { label: '多选二', value: 'value2' }
              ],
              showSelectAll: false,
              fetchRemote: false,
              remote: { url: '', label: '', value: '' },
              rules: [],
              showTip: false,
              tipContent: '提示文字'
            }
          },
          {
            id: 'Select_bnut',
            condition: true,
            componentName: 'Select',
            name: '下拉框',
            props: {
              submitKey: 'Select_bnut',
              title: '下拉框标题',
              defaultValue: '',
              value: '',
              disabled: false,
              multiple: false,
              allowClear: false,
              size: 'small',
              placeholder: '请输入',
              filterable: false,
              style: {},
              rules: [],
              options: [
                { label: '选项一', value: 'value1' },
                { label: '选项二', value: 'value2' }
              ],
              fetchRemote: false,
              remote: { url: '', label: '', value: '' },
              showTip: false,
              tipContent: '提示文字',
              isCommitLabel: false,
              commitLabelKey: '',
              appendToBody: false
            }
          },
          {
            id: 'InputNumber_azsj',
            condition: true,
            componentName: 'InputNumber',
            name: '数字输入框',
            props: {
              submitKey: 'InputNumber_azsj',
              title: '数字输入框',
              placeholder: '请输入',
              rules: [],
              style: {},
              controls: true,
              disabled: false,
              size: 'small',
              step: 1,
              controlsPosition: 'right',
              showTip: false,
              tipContent: '提示文字'
            }
          },
          {
            id: 'Switch_19py',
            condition: true,
            componentName: 'Switch',
            name: '开关',
            props: {
              submitKey: 'Switch_19py',
              title: '开关项标题',
              value: false,
              disabled: false,
              activeColor: '',
              inactiveColor: '',
              style: {},
              rules: [],
              showTip: false,
              tipContent: '提示文字'
            }
          },
          {
            id: 'TimePicker_sxpq',
            condition: true,
            componentName: 'TimePicker',
            name: '时间选择',
            props: {
              submitKey: 'TimePicker_sxpq',
              title: '时间选择器',
              value: '',
              isRange: false,
              disabled: false,
              allowClear: false,
              placeholder: '请选择时间',
              size: 'medium',
              startPlaceholder: '请选择开始时间',
              endPlaceholder: '请选择结束时间',
              valueFormat: 'timestamp',
              style: {},
              showTip: false,
              tipContent: '提示文字',
              rules: []
            }
          },
          {
            id: 'DatePicker_todz',
            condition: true,
            componentName: 'DatePicker',
            name: '日期选择',
            props: {
              submitKey: 'DatePicker_todz',
              title: '日期选择器',
              type: 'date',
              value: '',
              startTime: '',
              endTime: '',
              isRange: false,
              disabled: false,
              allowClear: false,
              placeholder: '请选择日期',
              size: 'medium',
              startPlaceholder: '请选择开始日期',
              endPlaceholder: '请选择结束日期',
              outFormatter: '',
              valueFormat: 'timestamp',
              rules: [],
              showTip: false,
              tipContent: '提示文字',
              style: {}
            }
          },
          {
            id: 'CascaderSelect_pwen',
            condition: true,
            componentName: 'CascaderSelect',
            name: '级联选择',
            props: {
              submitKey: 'CascaderSelect_pwen',
              title: '级联选择器',
              value: '',
              disabled: false,
              multiple: false,
              allowClear: false,
              size: 'small',
              collapseTags: true,
              placeholder: '请输入',
              filterable: false,
              style: {},
              rules: [],
              options: [
                {
                  value: 2974,
                  label: '西安',
                  children: [
                    { value: 2975, label: '西安市' },
                    { value: 2976, label: '高陵县' },
                    { value: 2977, label: '蓝田县' }
                  ]
                },
                {
                  value: 2975,
                  label: '西安11',
                  children: [
                    { value: 29751, label: '西安市1' },
                    { value: 29761, label: '高陵县1' },
                    { value: 29771, label: '蓝田县1' }
                  ]
                }
              ],
              fetchRemote: false,
              remote: { url: '', label: '', value: '', childrenKey: '' },
              showTip: false,
              tipContent: '提示文字'
            }
          },
          {
            id: 'Upload_iegg',
            condition: true,
            componentName: 'Upload',
            name: '上传',
            props: {
              submitKey: 'Upload_iegg',
              title: '上传项标题',
              style: {},
              uploadTitle: '上传文件',
              action: '',
              multiple: false,
              showTip: false,
              tip: '只能上传jpg/png文件，且不超过500kb',
              disabled: false,
              limit: null,
              name: 'file',
              showFileList: true,
              drag: false,
              buttonType: false,
              accept: '',
              listType: 'text',
              fileList: [],
              uploadName: 'file',
              uploadHeaders: '',
              uploadData: {},
              uploadWithCredentials: false
            }
          }
        ]
      }
    ],
    logicList: [
      {
        nodes: [
          {
            id: 'init_1azos4vjtni8000',
            type: 'event-node',
            x: 100,
            y: 80,
            properties: {
              componentId: 'page_init',
              componentName: 'pageInit',
              name: '页面初始化'
            }
          },
          {
            id: 'logic_98ujn64fwy00000',
            type: 'common-node',
            x: 260,
            y: 80,
            properties: {
              type: 'dataSource',
              name: '请求数据',
              componentName: 'dataSource'
            }
          },
          {
            id: 'logic_d5nttghd60o0000',
            type: 'common-node',
            x: 420,
            y: 80,
            properties: {
              type: 'pageJump',
              name: '页面跳转',
              componentName: 'pageJump'
            }
          },
          {
            id: 'logic_fsygrbs67t40000',
            type: 'common-node',
            x: 420,
            y: 140,
            properties: {
              type: 'dataConvert',
              name: '数据转换1',
              componentName: 'dataConvert',
              dc: {
                convertList: [
                  {
                    key: 'key1',
                    value: {
                      type: 'dataConvert',
                      nodeId: 'logic_9v5h5c4ium80000'
                    }
                  },
                  { key: 'key2' },
                  { key: 'key3' }
                ],
                convertCode: 'return [1, 2, 3]'
              }
            }
          },
          {
            id: 'logic_9v5h5c4ium80000',
            type: 'common-node',
            x: 580,
            y: 140,
            properties: {
              type: 'dataConvert',
              name: '数据转换2',
              componentName: 'dataConvert',
              dc: { convertList: [], convertCode: 'return [3, 4, 5]' }
            }
          },
          {
            id: 'logic_73gus8kpsgk0000',
            type: 'common-node',
            x: 260,
            y: 140,
            properties: {
              type: 'dataConvert',
              name: '数据转换',
              componentName: 'dataConvert',
              dc: {
                convertList: [
                  {
                    key: 'key1',
                    value: {
                      type: 'componentProp',
                      prop: 'value',
                      field: '',
                      componentId: 'InputNumber_azsj',
                      dataType: 'number',
                      componentName: '数字输入框',
                      propName: '当前值'
                    }
                  },
                  {
                    key: 'key2',
                    value: {
                      type: 'componentProp',
                      prop: 'value',
                      field: '',
                      componentId: 'TimePicker_sxpq',
                      dataType: 'number',
                      componentName: '时间选择器',
                      propName: '值'
                    }
                  },
                  {
                    key: '',
                    value: { type: 'dataConvert', dataType: 'string' }
                  }
                ],
                convertCode:
                  'const my_new_code_here = "Blabla"\n\nconsole.log(\'this.12123\')\n\nreturn my_new_code_here'
              }
            }
          }
        ],
        edges: [
          {
            id: 'logic_582qup4obxg0000',
            type: 'logic-line',
            sourceNodeId: 'logic_fsygrbs67t40000',
            targetNodeId: 'logic_9v5h5c4ium80000',
            startPoint: { x: 470, y: 140 },
            endPoint: { x: 530, y: 140 },
            properties: {},
            pointsList: [
              { x: 470, y: 140 },
              { x: 530, y: 140 }
            ]
          },
          {
            id: 'logic_3s6nbc92cx00000',
            type: 'logic-line',
            sourceNodeId: 'logic_98ujn64fwy00000',
            targetNodeId: 'logic_d5nttghd60o0000',
            startPoint: { x: 310, y: 80 },
            endPoint: { x: 370, y: 80 },
            properties: {},
            pointsList: [
              { x: 310, y: 80 },
              { x: 370, y: 80 }
            ]
          },
          {
            id: 'logic_93xrjtjbzs40000',
            type: 'logic-line',
            sourceNodeId: 'logic_98ujn64fwy00000',
            targetNodeId: 'logic_fsygrbs67t40000',
            startPoint: { x: 310, y: 80 },
            endPoint: { x: 370, y: 140 },
            properties: {},
            pointsList: [
              { x: 310, y: 80 },
              { x: 334, y: 80 },
              { x: 334, y: 140 },
              { x: 370, y: 140 }
            ]
          },
          {
            id: 'logic_fz4h8dc8yds0000',
            type: 'logic-line',
            sourceNodeId: 'init_1azos4vjtni8000',
            targetNodeId: 'logic_98ujn64fwy00000',
            startPoint: { x: 150, y: 80 },
            endPoint: { x: 210, y: 80 },
            properties: {},
            pointsList: [
              { x: 150, y: 80 },
              { x: 210, y: 80 }
            ]
          },
          {
            id: 'logic_2zcnfddo2ng0000',
            type: 'logic-line',
            sourceNodeId: 'init_1azos4vjtni8000',
            targetNodeId: 'logic_73gus8kpsgk0000',
            startPoint: { x: 150, y: 80 },
            endPoint: { x: 210, y: 140 },
            properties: {},
            pointsList: [
              { x: 150, y: 80 },
              { x: 174, y: 80 },
              { x: 174, y: 140 },
              { x: 210, y: 140 }
            ]
          }
        ]
      }
    ],
    componentsMap: [
      {
        package: 'suda-basic-material',
        componentName: 'SudaText',
        version: '0.0.1'
      },
      {
        package: 'suda-basic-material',
        componentName: 'SudaButton',
        version: '0.0.1'
      },
      {
        package: 'suda-basic-material',
        componentName: 'Container',
        version: '0.0.1'
      },
      {
        package: 'suda-basic-material',
        componentName: 'SudaImage',
        version: '0.0.1'
      },
      {
        package: 'suda-basic-material',
        componentName: 'Input',
        version: '0.0.3'
      },
      {
        package: 'suda-basic-material',
        componentName: 'Radio',
        version: '0.0.2'
      },
      {
        package: 'suda-basic-material',
        componentName: 'Checkbox',
        version: '0.0.3'
      },
      {
        package: 'suda-basic-material',
        componentName: 'Select',
        version: '0.0.4'
      },
      {
        package: 'suda-basic-material',
        componentName: 'InputNumber',
        version: '0.0.2'
      },
      {
        package: 'suda-basic-material',
        componentName: 'Switch',
        version: '0.0.2'
      },
      {
        package: 'suda-basic-material',
        componentName: 'TimePicker',
        version: '0.0.2'
      },
      {
        package: 'suda-basic-material',
        componentName: 'DatePicker',
        version: '0.0.5'
      },
      {
        package: 'suda-basic-material',
        componentName: 'CascaderSelect',
        version: '0.0.2'
      },
      {
        package: 'suda-basic-material',
        componentName: 'Upload',
        version: '0.0.2'
      }
    ],
    utils: [],
    version: '1.0.0'
  }
}
