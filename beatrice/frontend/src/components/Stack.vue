<script setup lang="ts">
interface Props {
  space?: string;
  recursive?: boolean;
}

withDefaults(defineProps<Props>(), {
  space: "var(--s1)",
  recursive: false,
});
</script>

<template>
  <div :class="[recursive ? $style.recursive : $style.stack]">
    <slot />
  </div>
</template>

<style module>
.stack,
.recursive {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.stack > * + *,
.recursive * + * {
  margin-block-start: v-bind(space);
}

.stack:only-child,
.recursive:only-child {
  block-size: 100%;
}
</style>
