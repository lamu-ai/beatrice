<script setup lang="ts">
import Sidebar from "@/components/Sidebar.vue";
import SidebarMenu from "@/components/SidebarMenu.vue";
</script>

<template>
  <Sidebar>
    <SidebarMenu />
    <div class="content"></div>
  </Sidebar>
</template>

<style>
@import "@/assets/style/base.css";

.content {
  background-color: var(--color-background-soft);
  min-height: 100vh;
}
</style>
