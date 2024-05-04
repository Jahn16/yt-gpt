<script lang="ts">
	import SvelteMarkdown from 'svelte-markdown';
	import type { ChatMessage } from '../models';

	export let message: ChatMessage;
</script>

<div class="col">
	<div class="card border-{message.author === 'bot' ? 'secondary' : 'success'}">
		<div class="card-body">
			<SvelteMarkdown source={message.content} />
		</div>
	</div>
</div>

<style>
	.card {
		padding: 0px;
		width: 60%;
		margin: auto;
	}
	.col {
		margin-top: 10px;
	}
</style>
