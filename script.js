const API_URL = "http://127.0.0.1:8000/cursos";
        let idParaDeletar = null;

        // Mapeamento de Ícones Devicon baseados na Categoria ou Título
        function obterIconeLinguagem(titulo) {
            const t = titulo.toLowerCase();
            if (t.includes("python")) return '<i class="devicon-python-plain colored"></i>';
            if (t.includes("javascript") || t.includes("js")) return '<i class="devicon-javascript-plain colored"></i>';
            if (t.includes("java")) return '<i class="devicon-java-plain colored"></i>';
            if (t.includes("c#") || t.includes("csharp")) return '<i class="devicon-csharp-plain colored"></i>';
            if (t.includes("php")) return '<i class="devicon-php-plain colored"></i>';
            if (t.includes("react")) return '<i class="devicon-react-original colored"></i>';
            if (t.includes("html") || t.includes("css")) return '<i class="devicon-html5-plain colored"></i>';
            if (t.includes("sql")) return '<i class="devicon-sqldeveloper-plain colored"></i>';
            return '<i class="devicon-code-style-plain" style="color: var(--primary);"></i>';
        }

        function showToast(msg) {
            const toast = document.getElementById("toast");
            toast.innerText = msg;
            toast.classList.add("show");
            setTimeout(() => toast.classList.remove("show"), 3000);
        }

        async function carregarCursos() {
            try {
                const inputBusca = document.getElementById("input-busca");
                const termo = inputBusca ? inputBusca.value.trim() : "";
                const url = termo ? `${API_URL}?q=${encodeURIComponent(termo)}` : API_URL;

                const resposta = await fetch(url);
                const cursos = await resposta.json();
                
                const tabela = document.getElementById("tabela-cursos");
                tabela.innerHTML = "";
                
                let totalAulas = 0;
                let totalHoras = 0;

                cursos.forEach(c => {
                    totalAulas += c.aulas;
                    totalHoras += c.horas;
                });

                document.getElementById("kpi-total").innerText = cursos.length;
                document.getElementById("kpi-aulas").innerText = totalAulas;
                document.getElementById("kpi-horas").innerText = `${totalHoras}h`;

                if(cursos.length === 0) {
                    tabela.innerHTML = `<tr><td colspan="4" style="text-align:center; color: var(--text-muted); padding: 32px;">Nenhum curso encontrado.</td></tr>`;
                    return;
                }

                cursos.forEach(curso => {
                    const tr = document.createElement("tr");
                    const termoIcone = curso.categoria || curso.titulo;
                    const icone = obterIconeLinguagem(termoIcone);
                    
                    tr.innerHTML = `
                        <td><span class="badge-id">#${curso.id}</span></td>
                        <td>
                            <div class="tech-cell">
                                ${icone}
                                <strong>${curso.titulo}</strong>
                            </div>
                        </td>
                        <td style="color: var(--text-muted);">${curso.aulas} aulas • ${curso.horas}h</td>
                        <td style="text-align: right;">
                            <button class="btn-edit btn-sm" onclick="prepararEdicao(${curso.id}, '${curso.titulo.replace(/'/g, "\\'")}', '${(curso.categoria || "Outros").replace(/'/g, "\\'")}', ${curso.aulas}, ${curso.horas})">Editar</button>
                            <button class="btn-delete btn-sm" onclick="abrirModalDeletar(${curso.id}, '${curso.titulo.replace(/'/g, "\\'")}')">Excluir</button>
                        </td>
                    `;
                    tabela.appendChild(tr);
                });
            } catch (err) {
                showToast("Erro ao conectar com a API!");
            }
        }

        async function salvarCurso() {
            const id = document.getElementById("curso-id").value;
            const titulo = document.getElementById("titulo").value;
            const categoria = document.getElementById("categoria").value;
            const aulas = parseInt(document.getElementById("aulas").value);
            const horas = parseInt(document.getElementById("horas").value);

            if (!titulo || isNaN(aulas) || isNaN(horas) || aulas <= 0 || horas <= 0) {
                showToast("Preencha todos os campos com valores válidos!");
                return;
            }

            const payload = { titulo, categoria, aulas, horas };

            try {
                if (id) {
                    await fetch(`${API_URL}/${id}`, {
                        method: "PUT",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(payload)
                    });
                    showToast("Curso atualizado com sucesso!");
                } else {
                    await fetch(API_URL, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(payload)
                    });
                    showToast("Curso cadastrado no banco!");
                }

                limparFormulario();
                carregarCursos();
            } catch (err) {
                showToast("Erro ao salvar curso!");
            }
        }

        function abrirModalDeletar(id, titulo) {
            idParaDeletar = id;
            document.getElementById("modal-msg").innerText = `Tem certeza que deseja remover o curso "#${id} - ${titulo}"?`;
            document.getElementById("delete-modal").classList.add("active");
        }

        function fecharModal() {
            idParaDeletar = null;
            document.getElementById("delete-modal").classList.remove("active");
        }

        document.getElementById("btn-confirm-action").onclick = async function() {
            if(idParaDeletar) {
                await fetch(`${API_URL}/${idParaDeletar}`, { method: "DELETE" });
                showToast("Curso removido com sucesso!");
                fecharModal();
                carregarCursos();
            }
        };

        function prepararEdicao(id, titulo, categoria, aulas, horas) {
            document.getElementById("curso-id").value = id;
            document.getElementById("titulo").value = titulo;
            document.getElementById("categoria").value = categoria || "Outros";
            document.getElementById("aulas").value = aulas;
            document.getElementById("horas").value = horas;

            document.getElementById("form-title").innerText = `Editar Curso #${id}`;
            document.getElementById("btn-submit").innerText = "Atualizar Curso";
            document.getElementById("btn-cancel").style.display = "inline-block";
        }

        function limparFormulario() {
            document.getElementById("form-title").innerText = "Cadastrar Novo Curso";
            document.getElementById("curso-id").value = "";
            document.getElementById("titulo").value = "";
            document.getElementById("categoria").value = "Python";
            document.getElementById("aulas").value = "";
            document.getElementById("horas").value = "";
            
            document.getElementById("btn-submit").innerText = "Salvar Curso";
            document.getElementById("btn-cancel").style.display = "none";
        }

        carregarCursos();