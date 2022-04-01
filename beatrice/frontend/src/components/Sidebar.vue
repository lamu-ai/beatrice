<script setup lang="ts">
interface Props {
  side?: "left" | "right";
  sideWidth?: string;
  contentMin?: string;
  space?: string;
  noStretch?: boolean;
}

withDefaults(defineProps<Props>(), {
  side: "left",
  sideWidth: "auto",
  contentMin: "50%",
  space: "var(--s1)",
  noStretch: false,
});
</script>

<template>
  <div
    :class="[$style.withSidebar, side == 'left' ? $style.left : $style.right]"
  >
    <slot />
  </div>
</template>

<style module>
.withSidebar {
  display: flex;
  flex-wrap: wrap;
  gap: v-bind(space);
  align-items: v-bind("noStretch ? 'flex-start' : 'stretch'");
}

.left > :first-child,
.right > :last-child {
  flex-basis: v-bind(sideWidth);
  flex-grow: 1;
}

.left > :last-child,
.right > :first-child {
  flex-basis: 0;
  flex-grow: 999;
  min-inline-size: v-bind(contentMin);
}
</style>
