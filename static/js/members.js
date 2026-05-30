document.addEventListener('alpine:init', () => {
  Alpine.data('membroForm', (initial = {}) => ({
    nome: initial.nome ?? '',
    email: initial.email ?? '',
    touched: { nome: false, email: false },

    get nomeError() {
      if (!this.touched.nome) return '';
      if (!this.nome.trim()) return 'Nome é obrigatório';
      if (this.nome.trim().length < 3) return 'Nome deve ter ao menos 3 caracteres';
      return '';
    },

    get emailError() {
      if (!this.touched.email) return '';
      if (this.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email)) return 'Email inválido';
      return '';
    },

    get formInvalid() {
      return !this.nome.trim() || this.nome.trim().length < 3 || this.emailError !== '';
    },

    submit(event) {
      this.touched.nome = true;
      this.touched.email = true;
      if (this.formInvalid) event.preventDefault();
    },
  }));
});
