describe('Teste de download de PDF', () => {
    beforeEach(() => {
      cy.visit('/');
      cy.get(':nth-child(1) > .nav-link').click();
      cy.get('#username').type('anton');
      cy.get('#password').type('123456');
      cy.get('button').click();
    });
  
    it('Deve fazer o download do PDF corretamente', () => {
      
      cy.get(':nth-child(1) > div > .button-3').click();
  
      cy.wait(5000);
  
      cy.task('listDownloads').then(downloads => {
        const downloadedPDF = downloads.find(download => download.endsWith('.pdf'));
        expect(downloadedPDF).to.exist
      });
    });
  });
  