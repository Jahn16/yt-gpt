<script lang="ts">
	import type { ChatMessage } from '../models';
	export let message: ChatMessage;
</script>

<div class="col">
	<div class="card border-{message.author === 'bot' ? 'secondary' : 'success'}">
		<div class="card-body">
			<p class="card-text">
				{message.content}
			</p>
		</div>
	</div>
</div>

<style>
	.card {
		padding: 0px;
    width: 90%;
    margin: auto;

	}
  .col {
    margin-top: 10px;
  }
</style>
