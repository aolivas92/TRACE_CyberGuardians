// src/routes/credGenAI/run/+page.server.js

/** @type {import('./$types').PageServerLoad} */
export async function load() {
	console.log("AI Generator +page.server.js triggered");

	// Simulated credentials from wordlist
	const tableData = [
		{ id: 1, username: '1234567890@!#$%^&*()', password: 'Abcdefghijklmnopqr' },
		{ id: 2, username: '0987654321%*&^@!()#', password: 'Uvwxzyzabcdefghijklm' },
		{ id: 3, username: '1122334455*()$#@!^', password: 'Opqrstuvwxyzabcdefg' },
		{ id: 4, username: '3344556677@!()#$', password: 'Xyabcdefghijklmnoqr' },
		{ id: 5, username: '9988776655@!#%^&*()', password: 'Tuvwxyzabcdefghioqr' },
		{ id: 6, username: '5544332211%*@!()#$', password: 'Pqrstuvwxyzabcdefgh' },
		{ id: 7, username: '9080706050$#@%*&@!()', password: 'Jklmnopqrstuvwxyza' }
	];

	const tableColumns = [
		{ key: 'id', label: 'ID' },
		{ key: 'username', label: 'Usernames' },
		{ key: 'password', label: 'Passwords' }
	];

	// These eventually come from the backend
	const metadata = {
		runningTime: 143.94,
		usernamesGenerated: 532,
		passwordsGenerated: 82
	};

	return {
		tableData,
		tableColumns,
		...metadata
	};
}