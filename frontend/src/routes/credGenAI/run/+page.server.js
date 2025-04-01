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
		{ id: 7, username: '9080706050$#@%*&@!()', password: 'Jklmnopqrstuvwxyza' },
		{ id: 8, username: '6677889900@!#$%^&*()', password: 'Cdefghijklmnopqrstuv' },
		{ id: 9, username: '7766554433%*&^@!()#', password: 'Wxyzabcdefghijklmnop' },
		{ id: 10, username: '8899001122*()$#@!^', password: 'Efghijklmnopqrstuvwxyz' },
		{ id: 11, username: '2233445566@!()#$%^', password: 'Ghijklmnopqrstuvwxyza' },
		{ id: 12, username: '4455667788@!#%^&*()', password: 'Ijklmnopqrstuvwxyzabcd' },
		{ id: 13, username: '6677889900%*@!()#$', password: 'Klmnopqrstuvwxyabcdef' },
		{ id: 14, username: '9988776655$#@%*&@!()', password: 'Mnopqrstuvwxyzabcdefg' }
	];

	const tableColumns = [
		{ key: 'id', label: 'ID' },
		{ key: 'username', label: 'Usernames' },
		{ key: 'password', label: 'Passwords' }
	];

	return {
		tableData,
		tableColumns,
	};
}