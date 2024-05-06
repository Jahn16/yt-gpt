<script lang="ts">
	import type { Chat } from '../models';
	import { submitChat } from '$lib/shareGPT';
	export let chat: Chat;
</script>

<div id="share">
	<button type="button" class="btn btn-light btn-sm" on:click={() => submitChat(chat)}
		>ShareGPT <i class="bi bi-share"></i></button
	>
</div>
