<script setup lang="ts">
interface Props {
  max?: string;
  andText?: boolean;
  gutters?: string;
  intrinsic?: boolean;
}

withDefaults(defineProps<Props>(), {
  max: "var(--measure)",
  andText: false,
  gutters: "0",
  intrinsic: false,
});
</script>

<template>
  <div
    :class="[
      $style.center,
      andText ? $style.andText : '',
      intrinsic ? $style.intrinsic : '',
    ]"
  >
    <slot />
  </div>
</template>

<style module>
.center {
  box-sizing: content-box;
  margin-inline: auto;
  max-inline-size: v-bind(max);
  padding-inline-start: v-bind(gutters);
  padding-inline-end: v-bind(gutters);
}

.andText {
  text-align: center;
}

.intrinsic {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
