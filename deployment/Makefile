# =====================
# Test
# =====================
test_ansible:
	cp ansible/Dockerfile Dockerfile
	docker build --force-rm=true --rm=true --no-cache .  
	rm Dockerfile
	docker rmi $$(docker images -q --filter dangling=true)