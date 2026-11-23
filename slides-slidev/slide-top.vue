<template>
  <footer class="page-number">{{ $page }}</footer>
</template>

<style scoped>
.page-number {
  position: absolute;
  right: 1.25rem;
  bottom: .5rem;
  color: #475569;
  font: 600 14px/1.2 'Be Vietnam Pro', sans-serif;
  font-variant-numeric: tabular-nums;
  pointer-events: none;
}
</style>
