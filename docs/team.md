---
layout: page
---

<script setup>
import {
  VPTeamPage,
  VPTeamPageTitle,
  VPTeamMembers
} from 'vitepress/theme'

const coreMembers = [
  {
    avatar: 'xd.png',
    name: '许队',
    title: 'Leader',
    desc: '团队主理人，负责团队整体规划和项目管理。有丰富的教学和项目管理经验，致力于指导团队成员成长。'
  },
  {
    avatar: 'hd.png',
    name: '黄队',
    title: 'Leader',  
    desc: '团队技术指导老师，为团队提供技术方向指导。在软件开发和教学方面有一定经验，乐于分享技术知识。'
  },
  {
    avatar: 'zhh.png',
    name: '詹皇浩',
    title: 'Leader、开发工程师',
    desc: '负责统筹项目和AIS终端伴侣开发工作。对项目管理和软件开发有浓厚兴趣，不断学习新技术。'
  },
  {
    avatar: 'cyc.png',
    name: '陈友诚',
    title: '开发工程师',
    desc: '主要负责AI大模型部署和调优工作。对人工智能技术充满热情，持续探索AI技术的实际应用。'
  },
  {
    avatar: 'hjh.png',
    name: '黄金鸿',
    title: '运维工程师',
    desc: '负责TIDB数据库管理和Docker部署相关工作。对数据库技术和容器化部署有一定了解，努力提升运维技能。'
  },
  {
    avatar: 'zjl.png',
    name: '周俊麒',
    title: '测试工程师',
    desc: '主要从事VUE数据可视化开发和录课制作工作。喜欢前端技术和教学视频制作，希望通过技术帮助更多人学习。'
  }
]
</script>

<VPTeamPage>
  <VPTeamPageTitle>
    <template #title>智学工坊</template>
    <template #lead>
      借助AI的智慧，让学习更高效<br/><br/>智学工坊是由中职学校新一代信息技术相关专业师生组成的团队。<br/>团队愿景是用技术改变学习方式，让学习者更好地掌握知识，提升技能，实现个人成长。
    </template>
    
  </VPTeamPageTitle>

  <VPTeamMembers size="medium" :members="coreMembers" />
</VPTeamPage>