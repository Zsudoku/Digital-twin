<!--
 * @Date: 2022-04-03 19:41:02
 * @LastEditors: ZSudoku
 * @LastEditTime: 2022-04-03 19:55:49
 * @FilePath: \Digita-twin\README.md
-->
git status
git add .
git commit -m "xxxx"
git pull origin
git pull upstream main
git push origin
github pull request


情景描述：

存在L个上货点,根据一定的规则,L个上货点最终交汇在一个点位，之后成箱的资产进入叠箱机，叠箱机将成箱的资产叠成垛，送往堆垛机入口处。
已知存在x个堆垛机，每个堆垛机有两个入口。
已知资产从叠箱机到每个堆垛机入口所消耗的时间，单位秒。
设，当前有n垛资产从叠箱机送往堆垛机。每个资产都有唯一的编号，即（1~n）,每个编号代表唯一的货位，则入库顺序为一个总数为n的排列。排列已知。

要求：由给出的排列，计算出每个垛资产到堆垛机入口的时间。