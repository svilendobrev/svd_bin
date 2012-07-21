void main(int ac, char**av, char**env) {
	if (env) while (*env) printf("%0x : %s\n",*env,*env),env++;
}
