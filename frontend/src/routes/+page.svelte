<!-- <script> -->
<!-- 	export let messages = []; -->

<!-- 	let newMessage = ''; -->
<!-- 	let transcription = ''; -->
<!-- 	const errorMessage = -->
<!-- 		'Oh no! It seems like we encountered an internal server error. 🛠️  Please try again later or contact support for assistance. Apologies for the inconvenience!'; -->
<!-- 	const sendMessage = async () => { -->
<!-- 		messages = [...messages, { author: 'user', content: newMessage }]; -->
<!-- 		if (!transcription) { -->
<!-- 			let youtubeUrl = newMessage; -->
<!-- 			newMessage = ''; -->
<!-- 			try { -->
<!-- 				transcription = await getTranscription(youtubeUrl); -->
<!-- 			} catch (error) { -->
<!-- 				console.log(error); -->
<!-- 				messages = [...messages, { author: 'bot', content: errorMessage }]; -->
<!-- 				return; -->
<!-- 			} -->
<!-- 			messages = [ -->
<!-- 				...messages, -->
<!-- 				{ -->
<!-- 					author: 'bot', -->
<!-- 					content: -->
<!-- 						"The transcription is complete. 🎉 Please feel free to ask me any questions you have about the video's content. Let's dive in!" -->
<!-- 				} -->
<!-- 			]; -->
<!-- 		} else { -->
<!-- 			let prompt = newMessage; -->
<!-- 			newMessage = ''; -->
<!-- 			messages = [...messages, { author: 'bot', content: GPTResponse }]; -->
<!-- 		} -->
<!-- 	}; -->

<!-- </script> -->

<script lang="ts">
	import Message from '../components/Message.svelte';
	import type { PageServerData } from './$types';

	export let data: PageServerData;
</script>

<div class=".container">
	<div class="row row-cols-1 row-cols-md-1 g-4">
		{#each data.chat as message}
			<Message {message} />{/each}
	</div>
	<div style="margin-top: 10px;">
		<form method="POST">
			<div class="input-group mb-3">
				<input
					name="message"
					type="text"
					class="form-control"
					placeholder="Enter your message"
					aria-label="Recipient's username"
					aria-describedby="button-addon2"
				/>
				<button class="btn btn-primary" type="submit" id="button-addon2">Submit</button>
			</div>
		</form>
	</div>
</div>

<style>
	#chat {
    margin-top: 20px;
		padding-bottom: 10px;
	}
  form {
    margin: auto;
    width: 90%;
  }
</style>
