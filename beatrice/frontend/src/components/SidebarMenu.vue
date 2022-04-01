<script setup lang="ts">
import { RouterLink } from "vue-router";

import Center from "@/components/Center.vue";
import Icon from "@/components/Icon.vue";
import Stack from "@/components/Stack.vue";

import IconLogo from "@/components/icons/IconLogo.vue";
import IconAnime from "@/components/icons/IconAnime.vue";
import IconManga from "@/components/icons/IconManga.vue";
import IconMovies from "@/components/icons/IconMovies.vue";
import IconTVSeries from "@/components/icons/IconTVSeries.vue";
import IconGames from "@/components/icons/IconGames.vue";
import IconMusic from "@/components/icons/IconMusic.vue";
import IconBooks from "@/components/icons/IconBooks.vue";

const space = "var(--s1)";
const sections = [
  { url: "/anime", name: "Anime" },
  { url: "/manga", name: "Manga" },
  { url: "/movies", name: "Movies" },
  { url: "/tvseries", name: "TV Series" },
  { url: "/games", name: "Games" },
  { url: "/music", name: "Music" },
  { url: "/books", name: "Books" },
];
</script>

<template>
  <nav>
    <RouterLink to="/">
      <Center intrinsic max="var(--s5)">
        <IconLogo />
        <span :class="$style.title">Beatrice</span>
      </Center>
    </RouterLink>

    <hr />

    <Stack space="var(--s-3)">
      <RouterLink
        v-for="section in sections"
        :key="section.url"
        :to="section.url"
      >
        <Icon :space="space">
          <template #icon>
            <IconAnime v-if="section.url === '/anime'" />
            <IconManga v-if="section.url === '/manga'" />
            <IconMovies v-if="section.url === '/movies'" />
            <IconTVSeries v-if="section.url === '/tvseries'" />
            <IconGames v-if="section.url === '/games'" />
            <IconMusic v-if="section.url === '/music'" />
            <IconBooks v-if="section.url === '/books'" />
          </template>
          <template #text>
            <span :class="$style.sectionName">{{ section.name }}</span>
          </template>
        </Icon>
      </RouterLink>
    </Stack>
  </nav>
</template>

<style module>
nav {
  padding: var(--s1) var(--s3) var(--s1);
  background: var(--color-background-dark);
}

a {
  padding-block: 0.25rem;
}

a:hover {
  background: #ebb4ab;
  margin-inline: calc(var(--s0) * -1);
  padding-inline: var(--s0);
  border-radius: var(--s1);
}

hr {
  border-color: var(--color-text);
  margin-block-end: var(--s1);
  margin-block-start: var(--s0);
}

.title {
  font-size: var(--s2);
  font-weight: bold;
  color: var(--color-accent);
}

.sectionName {
  text-transform: uppercase;
  font-weight: bold;
}
</style>
