<script setup lang="ts">
interface Props {
  space?: string;
  alignCenter?: boolean;
  width?: string;
  height?: string;
  fillColor?: string;
  label?: string;
}

withDefaults(defineProps<Props>(), {
  space: "",
  alignCenter: true,
  width: "0.8rem",
  height: "0.8rem",
  fillColor: "currentColor",
  label: "",
});
</script>

<template>
  <span
    :class="
      space
        ? alignCenter
          ? $style.withIconCenter
          : $style.withIconBaseline
        : ''
    "
    :role="label ? 'img' : ''"
    :aria-label="label"
  >
    <svg xmlns="http://www.w3.org/2000/svg" :class="$style.icon">
      <slot name="icon" />
    </svg>
    <slot name="text" />
  </span>
</template>

<style module>
.icon {
  width: v-bind(width);
  width: 1cap;
  height: v-bind(height);
  height: 1cap;
  fill: v-bind(fillColor);
}

.withIconBaseline {
  display: inline-flex;
  align-items: baseline;
}

.withIconCenter {
  display: inline-flex;
  align-items: center;
}

.withIconBaseline .icon,
.withIconCenter .icon {
  margin-inline-end: v-bind(space);
}
</style>
