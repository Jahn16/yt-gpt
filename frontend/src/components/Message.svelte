<script lang="ts">
	import SvelteMarkdown from 'svelte-markdown';
	import type { ChatMessage } from '../models';

	export let message: ChatMessage;
  const copyToClipboard = () => {
    navigator.clipboard.writeText(message.content);
  }
</script>

<div class="col">
	<div class="card border-{message.author === 'bot' ? 'secondary' : 'success'}">
		<div class="card-body">
			<SvelteMarkdown source={message.content} />

			<button id="copy" type="button" class="btn btn-link btn-sm" on:click={copyToClipboard}>
				<i class="bi bi-clipboard"></i>
			</button>
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
	#copy {
		float: right;
    padding: 0px;
	}
</style>
